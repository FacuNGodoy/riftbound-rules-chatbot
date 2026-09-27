"""Exporta el vault Riftbound a un grafo JSON validado para producción."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from generate_knowledge_vault import (
    BASE_DIR,
    CARDS_FILE,
    CATALOG_FILE,
    KNOWLEDGE_DIR,
    RULES_FILE,
    RULE_PATTERN,
    clean_text,
    compile_mechanics,
    knowledge_card_id,
    mechanics_for_text,
    parse_rule_sections,
    sha256_text,
)


OUTPUT_FILE = KNOWLEDGE_DIR / "knowledge_graph.json"
REPORT_FILE = KNOWLEDGE_DIR / "graph_validation.json"
SCHEMA_FILE = KNOWLEDGE_DIR / "schema.json"


def exact_rules(sections: list[dict]) -> dict[str, dict]:
    rules: dict[str, dict] = {}
    for section in sections:
        matches = list(RULE_PATTERN.finditer(section["body"]))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(section["body"])
            text = re.sub(r"\s+", " ", section["body"][match.start():end]).strip()
            rule_id = match.group("id")
            rules[rule_id] = {
                "id": f"rule:{rule_id}",
                "kind": "rule",
                "rule_id": rule_id,
                "section": section["number"],
                "section_title": section["title"],
                "text": text,
                "source": "docs/core_rules.md",
                "source_hash": sha256_text(text),
            }
    return rules


def provenance(source: str, locator: str, evidence: str) -> dict[str, str]:
    return {
        "source": source,
        "locator": locator,
        "evidence": re.sub(r"\s+", " ", evidence).strip()[:500],
    }


def edge(
    source: str,
    target: str,
    edge_type: str,
    edge_provenance: dict[str, str],
    confidence: str,
) -> dict[str, Any]:
    return {
        "source": source,
        "target": target,
        "type": edge_type,
        "provenance": edge_provenance,
        "confidence": confidence,
    }


def build_graph() -> dict[str, Any]:
    cards = json.loads(CARDS_FILE.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
    rules_text = RULES_FILE.read_text(encoding="utf-8")
    sections = parse_rule_sections(rules_text)
    rules = exact_rules(sections)
    compiled = compile_mechanics(catalog)

    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    for mechanic in catalog:
        mechanic_node_id = f"mechanic:{mechanic['id']}"
        nodes[mechanic_node_id] = {
            "id": mechanic_node_id,
            "kind": "mechanic",
            "mechanic_id": mechanic["id"],
            "title": mechanic["title"],
            "facts": mechanic["facts"],
            "patterns": mechanic["patterns"],
            "rule_ids": mechanic["rule_ids"],
            "relations": mechanic.get("relations", []),
            "source": "knowledge/mechanics_catalog.json",
            "source_hash": sha256_text(
                json.dumps(mechanic, sort_keys=True, ensure_ascii=False)
            ),
        }

    for rule in rules.values():
        nodes[rule["id"]] = rule

    for card in cards:
        card_id = knowledge_card_id(card)
        node_id = f"card:{card_id}"
        text = clean_text(card)
        mechanic_ids = mechanics_for_text(text, compiled)
        nodes[node_id] = {
            "id": node_id,
            "kind": "card",
            "card_id": card_id,
            "printed_number": card.get("card_number", ""),
            "name": card.get("name", card_id),
            "card_type": card.get("type", ""),
            "set": card.get("set", ""),
            "domains": card.get("domains", []),
            "tags": card.get("tags", []),
            "text": card.get("description") or card.get("rules_text") or "",
            "effect_text": card.get("effect_text", ""),
            "might_bonus": card.get("might_bonus", ""),
            "mechanics": mechanic_ids,
            "source": "cards.json",
            "source_hash": sha256_text(text),
        }
        for mechanic_id in mechanic_ids:
            mechanic = next(item for item in catalog if item["id"] == mechanic_id)
            matched_pattern = next(
                (
                    pattern
                    for pattern in mechanic["patterns"]
                    if re.search(pattern, text, re.IGNORECASE)
                ),
                mechanic["patterns"][0],
            )
            edges.append(
                edge(
                    node_id,
                    f"mechanic:{mechanic_id}",
                    "USES_MECHANIC",
                    provenance(
                        "cards.json",
                        card_id,
                        f"Patrón {matched_pattern!r} en el texto oficial de {card.get('name', card_id)}.",
                    ),
                    "exact",
                )
            )

    for mechanic in catalog:
        mechanic_node_id = f"mechanic:{mechanic['id']}"
        for rule_id in mechanic["rule_ids"]:
            edges.append(
                edge(
                    mechanic_node_id,
                    f"rule:{rule_id}",
                    "GOVERNED_BY",
                    provenance(
                        "knowledge/mechanics_catalog.json",
                        mechanic["id"],
                        f"La mecánica {mechanic['title']} está gobernada por la regla {rule_id}.",
                    ),
                    "curated",
                )
            )
        for relation in mechanic.get("relations", []):
            target = relation["target"]
            if target not in nodes:
                kind, _, slug = target.partition(":")
                nodes[target] = {
                    "id": target,
                    "kind": relation["target_kind"],
                    "title": slug.replace("-", " ").capitalize(),
                    "source": "knowledge/mechanics_catalog.json",
                }
            edges.append(
                edge(
                    mechanic_node_id,
                    target,
                    relation["type"],
                    provenance(
                        "knowledge/mechanics_catalog.json",
                        f"{mechanic['id']}.relations",
                        f"{relation['label']} (regla {relation['rule_id']}).",
                    ),
                    "curated",
                )
            )

    nodes_list = sorted(nodes.values(), key=lambda item: item["id"])
    edges.sort(key=lambda item: (item["source"], item["type"], item["target"]))
    return {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "cards.json": sha256_text(CARDS_FILE.read_text(encoding="utf-8")),
            "docs/core_rules.md": sha256_text(rules_text),
            "knowledge/mechanics_catalog.json": sha256_text(
                CATALOG_FILE.read_text(encoding="utf-8")
            ),
        },
        "nodes": nodes_list,
        "edges": edges,
    }


def validate_graph(graph: dict[str, Any]) -> dict[str, Any]:
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    allowed_edge_types = set(schema["edge_types"])
    allowed_confidence = set(schema["confidence_values"])
    errors: list[str] = []
    warnings: list[str] = []

    node_ids = [node.get("id", "") for node in graph["nodes"]]
    node_id_set = set(node_ids)
    duplicate_nodes = sorted(
        node_id for node_id in node_id_set if node_ids.count(node_id) > 1
    )
    if duplicate_nodes:
        errors.append(f"Nodos duplicados: {duplicate_nodes[:10]}")
    if "" in node_id_set:
        errors.append("Hay nodos sin ID.")

    edge_keys: set[tuple[str, str, str]] = set()
    for index, item in enumerate(graph["edges"]):
        label = f"edge[{index}]"
        source = item.get("source", "")
        target = item.get("target", "")
        edge_type = item.get("type", "")
        if source not in node_id_set:
            errors.append(f"{label}: source inexistente {source!r}.")
        if target not in node_id_set:
            errors.append(f"{label}: target inexistente {target!r}.")
        if edge_type not in allowed_edge_types:
            errors.append(f"{label}: tipo no permitido {edge_type!r}.")
        if item.get("confidence") not in allowed_confidence:
            errors.append(f"{label}: confidence inválida {item.get('confidence')!r}.")
        edge_provenance = item.get("provenance")
        if not isinstance(edge_provenance, dict) or not all(
            edge_provenance.get(key) for key in ("source", "locator", "evidence")
        ):
            errors.append(f"{label}: procedencia incompleta.")
        key = (source, edge_type, target)
        if key in edge_keys:
            warnings.append(f"Relación duplicada: {key}.")
        edge_keys.add(key)

    counts: dict[str, int] = {}
    for node in graph["nodes"]:
        counts[node["kind"]] = counts.get(node["kind"], 0) + 1
    if counts.get("card") != 960:
        errors.append(f"Se esperaban 960 cartas y hay {counts.get('card', 0)}.")

    catalog = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
    for mechanic in catalog:
        for rule_id in mechanic["rule_ids"]:
            if f"rule:{rule_id}" not in node_id_set:
                errors.append(
                    f"{mechanic['id']}: referencia la regla inexistente {rule_id}."
                )
        for relation in mechanic.get("relations", []):
            if f"rule:{relation['rule_id']}" not in node_id_set:
                errors.append(
                    f"{mechanic['id']}: relación respaldada por regla inexistente "
                    f"{relation['rule_id']}."
                )

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "nodes": len(graph["nodes"]),
            "edges": len(graph["edges"]),
            "node_kinds": counts,
            "edge_types": {
                edge_type: sum(
                    1 for item in graph["edges"] if item["type"] == edge_type
                )
                for edge_type in sorted(allowed_edge_types)
            },
        },
    }


def main() -> None:
    graph = build_graph()
    report = validate_graph(graph)
    REPORT_FILE.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    if not report["valid"]:
        for error in report["errors"]:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    OUTPUT_FILE.write_text(
        json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(
        f"Grafo válido: {report['stats']['nodes']} nodos, "
        f"{report['stats']['edges']} relaciones, "
        f"{OUTPUT_FILE.stat().st_size / 1024 / 1024:.2f} MB."
    )


if __name__ == "__main__":
    main()
