"""Genera un vault de Obsidian reproducible desde cartas y reglas oficiales.

Esta etapa solo crea notas y el esquema de datos. No modifica ChromaDB ni el
runtime del chatbot. Los directorios cards/, rules/ y mechanics/ son generados:
la fuente editable de las mecánicas es knowledge/mechanics_catalog.json.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import unicodedata
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
CARDS_FILE = BASE_DIR / "cards.json"
RULES_FILE = BASE_DIR / "docs" / "core_rules.md"
CATALOG_FILE = KNOWLEDGE_DIR / "mechanics_catalog.json"

GENERATED_DIRS = {
    "cards": KNOWLEDGE_DIR / "cards",
    "rules": KNOWLEDGE_DIR / "rules",
    "mechanics": KNOWLEDGE_DIR / "mechanics",
}

SECTION_PATTERN = re.compile(
    r"^###\s+(?P<number>\d{3})\.\s+(?P<title>.+?)\s*$", re.MULTILINE
)
RULE_PATTERN = re.compile(
    r"^(?:\*\*)?(?P<id>\d{3}(?:\.(?:\d+|[a-z]))*)\.(?:\*\*)?",
    re.MULTILINE,
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()).strip("-")


def knowledge_card_id(card: dict) -> str:
    printed = card.get("card_number", "").strip()
    if printed:
        return printed
    return "UNNUMBERED-" + "-".join(
        filter(
            None,
            [
                slugify(card.get("set", "unknown")),
                slugify(card.get("name", "card")),
                slugify(card.get("type", "")),
            ],
        )
    )


def rule_note_name(section: dict) -> str:
    safe_title = re.sub(r'[<>:"/\\|?*]+', " -", section["title"])
    safe_title = re.sub(r"\s+", " ", safe_title).strip(" .")
    return f"{section['number']} {safe_title}"


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(yaml_string(value) for value in values) + "]"


def frontmatter(properties: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in properties.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, list):
            rendered = yaml_list([str(item) for item in value])
        elif isinstance(value, (int, float)):
            rendered = str(value)
        else:
            rendered = yaml_string(str(value))
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    return "\n".join(lines)


def clean_text(card: dict) -> str:
    values = [
        card.get("name", ""),
        card.get("type", ""),
        " ".join(card.get("tags", [])),
        card.get("rules_text", ""),
        card.get("effect_text", ""),
        card.get("description", ""),
    ]
    return "\n".join(value for value in values if value)


def parse_rule_sections(text: str) -> list[dict]:
    matches = list(SECTION_PATTERN.finditer(text))
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end].strip()
        rule_ids = [item.group("id") for item in RULE_PATTERN.finditer(body)]
        sections.append(
            {
                "number": match.group("number"),
                "title": match.group("title"),
                "body": body,
                "rule_ids": rule_ids,
            }
        )
    return sections


def compile_mechanics(catalog: list[dict]) -> dict[str, list[re.Pattern]]:
    return {
        mechanic["id"]: [
            re.compile(pattern, re.IGNORECASE) for pattern in mechanic["patterns"]
        ]
        for mechanic in catalog
    }


def mechanics_for_text(
    text: str,
    compiled: dict[str, list[re.Pattern]],
) -> list[str]:
    return sorted(
        mechanic_id
        for mechanic_id, patterns in compiled.items()
        if any(pattern.search(text) for pattern in patterns)
    )


def reset_generated_dirs() -> None:
    for path in GENERATED_DIRS.values():
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def write_card_notes(
    cards: list[dict],
    catalog_by_id: dict[str, dict],
    compiled: dict[str, list[re.Pattern]],
) -> dict[str, list[str]]:
    card_mechanics: dict[str, list[str]] = {}
    for card in cards:
        card_number = knowledge_card_id(card)
        text = clean_text(card)
        mechanic_ids = mechanics_for_text(text, compiled)
        card_mechanics[card_number] = mechanic_ids
        mechanic_links = [
            f"[[mechanics/{mechanic_id}|{catalog_by_id[mechanic_id]['title']}]]"
            for mechanic_id in mechanic_ids
        ]
        properties = {
            "title": card.get("name", card_number),
            "id": card_number,
            "kind": "card",
            "printed_number": card.get("card_number", ""),
            "card_type": card.get("type", ""),
            "set": card.get("set", ""),
            "tags": ["riftbound", "knowledge/card"],
            "aliases": [card.get("name", "")],
            "source": "cards.json",
            "source_hash": sha256_text(text),
            "generated": True,
            "confidence": "exact",
        }
        lines = [
            frontmatter(properties),
            "",
            f"# {card.get('name', card_number)}",
            "",
            (
                f"**Número:** `{card.get('card_number')}`"
                if card.get("card_number")
                else f"**ID interno:** `{card_number}` (sin número impreso)"
            ),
            f"**Tipo:** {card.get('type', '—') or '—'}",
            f"**Set:** {card.get('set', '—') or '—'}",
        ]
        domains = card.get("domains", [])
        if domains:
            lines.append(f"**Dominios:** {', '.join(domains)}")
        stats = [
            f"Energy {card.get('energy')}" if card.get("energy") not in ("", "0", None) else "",
            f"Power {card.get('power')}" if card.get("power") not in ("", "0", None) else "",
            f"Might {card.get('might')}" if card.get("might") not in ("", "0", None) else "",
        ]
        stats = [stat for stat in stats if stat]
        if stats:
            lines.append(f"**Stats:** {', '.join(stats)}")
        lines.extend(["", "## Texto"])
        rules_text = card.get("rules_text") or card.get("description") or "Sin texto."
        lines.extend(["", rules_text])
        if card.get("effect_text"):
            lines.extend(["", "## Effect text", "", card["effect_text"]])
        if card.get("might_bonus"):
            lines.extend(["", f"**Might Bonus:** {card['might_bonus']}"])
        lines.extend(["", "## Mecánicas relacionadas", ""])
        lines.extend([f"- {link}" for link in mechanic_links] or ["- Sin mecánica catalogada."])
        lines.extend(
            [
                "",
                "> [!INFO] Nota generada",
                "> Regenerar con `python generate_knowledge_vault.py`; no editar manualmente.",
                "",
            ]
        )
        (GENERATED_DIRS["cards"] / f"{card_number}.md").write_text(
            "\n".join(lines), encoding="utf-8"
        )
    return card_mechanics


def write_rule_notes(
    sections: list[dict],
    catalog: list[dict],
) -> dict[str, str]:
    rule_to_section = {
        rule_id: section["number"]
        for section in sections
        for rule_id in section["rule_ids"]
    }
    relevant_sections = {
        rule_to_section[rule_id]
        for mechanic in catalog
        for rule_id in mechanic["rule_ids"]
        if rule_id in rule_to_section
    }
    for section in sections:
        if section["number"] not in relevant_sections:
            continue
        related = [
            mechanic
            for mechanic in catalog
            if any(
                rule_to_section.get(rule_id) == section["number"]
                for rule_id in mechanic["rule_ids"]
            )
        ]
        properties = {
            "title": f"{section['number']}. {section['title']}",
            "id": f"rule-section:{section['number']}",
            "kind": "rule-section",
            "tags": ["riftbound", "knowledge/rule"],
            "source": "docs/core_rules.md",
            "source_hash": sha256_text(section["body"]),
            "generated": True,
            "confidence": "official",
        }
        lines = [
            frontmatter(properties),
            "",
            f"# {section['number']}. {section['title']}",
            "",
            "> [!NOTE] Fuente oficial",
            "> Sección extraída de `docs/core_rules.md`.",
            "",
            section["body"],
            "",
            "## Mecánicas relacionadas",
            "",
        ]
        lines.extend(
            f"- [[mechanics/{mechanic['id']}|{mechanic['title']}]]"
            for mechanic in related
        )
        lines.append("")
        (GENERATED_DIRS["rules"] / f"{rule_note_name(section)}.md").write_text(
            "\n".join(lines), encoding="utf-8"
        )
    return rule_to_section


def write_mechanic_notes(
    catalog: list[dict],
    cards: list[dict],
    card_mechanics: dict[str, list[str]],
    rule_to_section: dict[str, str],
    sections: list[dict],
) -> None:
    section_by_number = {section["number"]: section for section in sections}
    cards_by_number = {
        knowledge_card_id(card): card for card in cards
    }
    for mechanic in catalog:
        card_ids = sorted(
            card_id
            for card_id, mechanics in card_mechanics.items()
            if mechanic["id"] in mechanics
        )
        properties = {
            "title": mechanic["title"],
            "id": f"mechanic:{mechanic['id']}",
            "kind": "mechanic",
            "tags": ["riftbound", "knowledge/mechanic"],
            "source": "knowledge/mechanics_catalog.json",
            "generated": True,
            "confidence": "curated",
        }
        lines = [
            frontmatter(properties),
            "",
            f"# {mechanic['title']}",
            "",
            "## Hechos validados",
            "",
        ]
        lines.extend(f"- {fact}" for fact in mechanic["facts"])
        lines.extend(["", "## Reglas", ""])
        for rule_id in mechanic["rule_ids"]:
            section_number = rule_to_section.get(rule_id)
            if not section_number:
                lines.append(f"- Regla `{rule_id}` (no encontrada)")
                continue
            section = section_by_number[section_number]
            note = rule_note_name(section)
            lines.append(f"- [[rules/{note}|Regla {rule_id}]]")
        lines.extend(["", f"## Cartas ({len(card_ids)})", ""])
        preview = card_ids[:80]
        lines.extend(
            f"- [[cards/{card_id}|{cards_by_number[card_id].get('name', card_id)} ({card_id})]]"
            for card_id in preview
        )
        if len(card_ids) > len(preview):
            lines.append(f"- …y {len(card_ids) - len(preview)} cartas más en el grafo exportado.")
        lines.append("")
        (GENERATED_DIRS["mechanics"] / f"{mechanic['id']}.md").write_text(
            "\n".join(lines), encoding="utf-8"
        )


def write_schema() -> None:
    schema = {
        "version": 1,
        "node_kinds": {
            "card": {
                "id": "número impreso o ID interno estable para tokens sin número",
                "required": ["id", "name", "text", "mechanics", "source"],
            },
            "rule": {
                "id": "número exacto de regla",
                "required": ["id", "text", "section", "source"],
            },
            "mechanic": {
                "id": "slug estable",
                "required": ["id", "title", "facts", "source"],
            },
        },
        "edge_types": {
            "USES_MECHANIC": "card -> mechanic",
            "GOVERNED_BY": "mechanic -> rule",
            "TRIGGERS_AFTER": "mechanic -> mechanic|event",
            "OCCURS_BEFORE": "mechanic|event -> mechanic|event",
            "RESOLVES_BEFORE": "mechanic|event -> mechanic|event",
            "READS_CURRENT_VALUE": "card|mechanic -> property",
            "REPLACES": "card|mechanic -> mechanic|event",
            "PREVENTS": "card|mechanic -> mechanic|event",
            "REQUIRES": "card|mechanic -> mechanic|event|property",
            "TARGETS": "card|mechanic -> object-kind",
            "MODIFIES": "card|mechanic -> property",
            "LINKED_TO": "card|rule|mechanic -> card|rule|mechanic",
        },
        "edge_required": ["source", "target", "type", "provenance", "confidence"],
        "confidence_values": ["exact", "curated", "inferred", "ambiguous"],
    }
    (KNOWLEDGE_DIR / "schema.json").write_text(
        json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_index(cards_count: int, rules_count: int, mechanics_count: int) -> None:
    text = f"""---
title: Riftbound Knowledge Vault
id: knowledge:index
kind: index
tags: [riftbound, knowledge/index]
status: active
---

# Riftbound Knowledge Vault

> [!INFO] Estado
> Vault generado desde fuentes versionadas: **{cards_count} cartas**, **{rules_count} secciones de reglas** y **{mechanics_count} mecánicas**.

## Navegación

- [[mechanics/play-trigger|Triggers al jugar]]
- [[mechanics/triggered-ability|Triggered abilities]]
- [[mechanics/chain|Chain y resolución]]
- [[mechanics/target|Targets y elecciones]]
- [[mechanics/replacement|Replacement effects]]
- [[mechanics/might|Might actual]]

## Fuentes

- Cartas: `cards.json`
- Reglamento: `docs/core_rules.md`
- Catálogo curado: `knowledge/mechanics_catalog.json`

> [!WARNING] Contenido generado
> Las carpetas `cards/`, `rules/` y `mechanics/` se regeneran por completo. Editar el catálogo fuente, no las notas resultantes.
"""
    (KNOWLEDGE_DIR / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    cards = json.loads(CARDS_FILE.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
    rules_text = RULES_FILE.read_text(encoding="utf-8")
    sections = parse_rule_sections(rules_text)
    compiled = compile_mechanics(catalog)
    catalog_by_id = {item["id"]: item for item in catalog}

    reset_generated_dirs()
    card_mechanics = write_card_notes(cards, catalog_by_id, compiled)
    rule_to_section = write_rule_notes(sections, catalog)
    write_mechanic_notes(
        catalog, cards, card_mechanics, rule_to_section, sections
    )
    write_schema()

    generated_rule_notes = len(list(GENERATED_DIRS["rules"].glob("*.md")))
    write_index(len(card_mechanics), generated_rule_notes, len(catalog))
    print(
        "Vault generado: "
        f"{len(card_mechanics)} cartas, "
        f"{generated_rule_notes} secciones de reglas, "
        f"{len(catalog)} mecánicas."
    )


if __name__ == "__main__":
    main()
