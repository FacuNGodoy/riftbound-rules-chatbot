"""
Runner de evaluación: corre los casos de eval/judge_cases.json contra el servidor
y reporta aciertos de veredicto y de citas.

Requiere el server levantado (por defecto en http://127.0.0.1:8004).

Uso:
    python eval/run_eval.py                  # todos los casos
    python eval/run_eval.py --case 7         # un caso puntual
    python eval/run_eval.py --delay 20       # más margen entre casos
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import requests

BASE_DIR = Path(__file__).parent
CASES_FILE = BASE_DIR / "judge_cases.json"
RESULTS_FILE = BASE_DIR / "results.json"


def grade(case: dict, resp: dict) -> dict:
    """Compara la respuesta del bot contra lo esperado del caso."""
    verdict = (resp.get("verdict") or "").upper()
    expected = case.get("expected_verdict")

    # expected_verdict null = caso de respuesta mixta o informativa (6 y 7):
    # no se puede puntuar por SI/NO, solo por las reglas citadas.
    verdict_ok = None if expected is None else verdict == expected.upper()

    # Citar 320 en la evidencia vale igual que nombrarla en el texto de la respuesta.
    titles = [c.get("title", "") for c in resp.get("citations", [])]
    haystack = " ".join([resp.get("answer", ""), *titles])

    # Cada entrada de must_mention puede ser una regla ("206") o una lista de reglas
    # igualmente válidas (["710", "137.3"]): en ese caso alcanza con que cite una.
    found, missing = [], []
    for requirement in case.get("must_mention", []):
        options = requirement if isinstance(requirement, list) else [requirement]
        hit = next((rule for rule in options if rule in haystack), None)
        (found if hit else missing).append(hit or " o ".join(options))

    # Abstenerse no es acertar. Sin esto un NO_RESUELTO que dice "me falta la regla 464"
    # cuenta como acierto solo porque el número aparece en el texto.
    abstained = verdict == "NO_RESUELTO"

    return {
        "verdict": verdict,
        "expected_verdict": expected,
        "verdict_ok": verdict_ok,
        "confidence": resp.get("confidence", ""),
        "citations": len(titles),
        "citation_titles": titles,
        "rules_found": found,
        "rules_missing": missing,
        "passed": not abstained and verdict_ok is not False and not missing,
        "answer": resp.get("answer", ""),
    }


def run_case(base_url: str, case: dict) -> dict:
    requests.post(f"{base_url}/reset", timeout=30).raise_for_status()
    resp = requests.post(
        f"{base_url}/ask", data={"query": case["question"]}, timeout=300
    )
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8004")
    parser.add_argument("--case", type=int, help="correr solo este id")
    parser.add_argument(
        "--delay",
        type=float,
        default=10.0,
        help="segundos de espera entre casos (cuota por minuto de Gemini)",
    )
    args = parser.parse_args()

    try:
        config = requests.get(f"{args.base_url}/config", timeout=10).json()
    except Exception as exc:
        print(f"No pude leer /config ({exc}). ¿Está levantado el server?")
        return

    cases = json.loads(CASES_FILE.read_text(encoding="utf-8"))
    if args.case:
        cases = [c for c in cases if c["id"] == args.case]
    if not cases:
        print("Ningún caso para correr.")
        return

    print(f"draft:    {', '.join(config['draft_models'])}")
    print(f"verifier: {', '.join(config['verifier_models'])}")
    if config.get("draft_override"):
        print("AVISO: override de draft activo, este resultado no es el de producción.")

    results = []
    for i, case in enumerate(cases):
        print(f"\n[{case['id']}] {case['question'][:90]}")
        try:
            res = grade(case, run_case(args.base_url, case))
        except Exception as exc:
            print(f"    ERROR: {exc}")
            res = {
                "verdict": "",
                "expected_verdict": case.get("expected_verdict"),
                "verdict_ok": False,
                "confidence": "",
                "citations": 0,
                "citation_titles": [],
                "rules_found": [],
                "rules_missing": case.get("must_mention", []),
                "passed": False,
                "answer": "",
                "error": str(exc),
            }

        results.append(
            {
                "id": case["id"],
                "tags": case["tags"],
                "deterministic": case.get("deterministic", False),
                **res,
            }
        )
        print(
            f"    {'OK  ' if res['passed'] else 'FAIL'} "
            f"veredicto={res['verdict'] or '-'} "
            f"esperado={case.get('expected_verdict') or 'n/a'} "
            f"conf={res['confidence'] or '-'} citas={res['citations']}"
        )
        if res["rules_missing"]:
            print(f"    faltan reglas: {', '.join(res['rules_missing'])}")

        if i < len(cases) - 1:
            time.sleep(args.delay)

    # Los casos interceptados por deterministic_ruling() no pasan por el LLM:
    # cuentan aparte para no inflar el porcentaje del pipeline.
    llm = [r for r in results if not r["deterministic"]]
    det = [r for r in results if r["deterministic"]]
    passed = sum(1 for r in llm if r["passed"])
    total = len(llm)
    pct = 100 * passed / total if total else 0.0

    print("\n" + "=" * 74)
    header = f"{'id':<5}{'veredicto':<14}{'esperado':<12}{'conf':<8}{'citas':<7}{'res'}"
    print(header)
    print("-" * 74)
    for r in results:
        flag = " *" if r["deterministic"] else ""
        print(
            f"{str(r['id']) + flag:<5}{r['verdict'] or '-':<14}"
            f"{r['expected_verdict'] or 'n/a':<12}"
            f"{r['confidence'] or '-':<8}{r['citations']:<7}"
            f"{'OK' if r['passed'] else 'FAIL'}"
        )
    print("-" * 74)
    print(f"Pipeline LLM: {passed}/{total} ({pct:.1f}%)")
    if det:
        det_ok = sum(1 for r in det if r["passed"])
        print(f"Determinísticos (*): {det_ok}/{len(det)} — no pasan por el modelo")

    RESULTS_FILE.write_text(
        json.dumps(
            {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "config": config,
                "passed": passed,
                "total": total,
                "pct": round(pct, 1),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Detalle en {RESULTS_FILE}")


if __name__ == "__main__":
    main()
