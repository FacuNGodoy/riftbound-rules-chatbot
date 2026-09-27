"""Resolvedor en memoria para interacciones cubiertas por el grafo Riftbound."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


MAX_MECHANICS = 8
MAX_RULES = 12

QUESTION_HINTS = {
    "play": ["juega", "jugar", "play", "spell", "hechizo"],
    "play-trigger": ["cuando juega", "cuando un jugador", "plays a spell", "juega el spell"],
    "triggered-ability": ["trigger", "dispara", "habilidad"],
    "chain": ["chain", "resolver", "resuelve", "antes", "después"],
    "target": ["target", "elige", "elegir", "objetivo"],
    "kill": ["mata", "matar", "muere", "kill", "die"],
    "might": ["might", "+1", "fuerza"],
    "counter": ["counter", "counterea", "cancela"],
    "repeat": ["repeat"],
    "replacement": ["reemplaza", "instead", "en vez"],
    "linked-instruction": ["if you do", "si lo hace", "si hacés", "si haces"],
    "reaction": ["reaction", "reacción", "respuesta"],
    "action": ["action", "acción"],
    "deal": ["daño", "damage", "deal"],
    "draw": ["roba", "robar", "draw"],
    "move": ["mueve", "mover", "move"],
    "attach": ["attach", "equipa", "equipment", "gear"],
    "printed-cost": ["coste", "costo", "cost"],
    "additional-cost": ["coste adicional", "costo adicional", "additional cost"],
}

CAUSAL_PRIORITY = [
    "play-trigger",
    "counter",
    "repeat",
    "replacement",
    "linked-instruction",
    "additional-cost",
    "triggered-ability",
    "chain",
    "target",
    "kill",
    "might",
    "reaction",
    "action",
    "attach",
    "deal",
    "move",
    "draw",
    "printed-cost",
    "play",
]
PRIORITY_INDEX = {
    mechanic_id: index for index, mechanic_id in enumerate(CAUSAL_PRIORITY)
}


class KnowledgeResolver:
    def __init__(self, graph_path: Path):
        self.graph_path = graph_path
        self.enabled = graph_path.exists()
        self.nodes: dict[str, dict] = {}
        self.outgoing: dict[str, list[dict]] = {}
        if not self.enabled:
            return
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        self.nodes = {node["id"]: node for node in graph["nodes"]}
        for item in graph["edges"]:
            self.outgoing.setdefault(item["source"], []).append(item)

    def _card_node(self, card: dict) -> dict | None:
        card_id = card.get("card_number", "").strip()
        if not card_id:
            return None
        return self.nodes.get(f"card:{card_id}")

    def _score_mechanic(
        self,
        mechanic_id: str,
        query: str,
        card_count: int,
        appearances: int,
    ) -> int:
        score = appearances * 2
        if appearances == card_count:
            score += 5
        if any(hint in query for hint in QUESTION_HINTS.get(mechanic_id, [])):
            score += 7
        node = self.nodes.get(f"mechanic:{mechanic_id}", {})
        if node.get("relations"):
            score += 3
        return score

    def resolve(self, query: str, cards: list[dict]) -> dict[str, Any] | None:
        if not self.enabled:
            return None
        card_nodes = []
        seen = set()
        for card in cards:
            node = self._card_node(card)
            if node and node["id"] not in seen:
                seen.add(node["id"])
                card_nodes.append(node)
        if len(card_nodes) < 2:
            return None

        appearances: dict[str, int] = {}
        for node in card_nodes:
            for mechanic_id in node.get("mechanics", []):
                appearances[mechanic_id] = appearances.get(mechanic_id, 0) + 1

        q = query.lower()
        ranked = sorted(
            appearances,
            key=lambda mechanic_id: (
                -self._score_mechanic(
                    mechanic_id, q, len(card_nodes), appearances[mechanic_id]
                ),
                PRIORITY_INDEX.get(mechanic_id, 999),
                mechanic_id,
            ),
        )
        selected_ids = ranked[:MAX_MECHANICS]
        mechanic_nodes = [
            self.nodes[f"mechanic:{mechanic_id}"] for mechanic_id in selected_ids
        ]
        relations = [
            relation
            for node in mechanic_nodes
            for relation in node.get("relations", [])
        ]
        if not relations:
            return None

        prioritized_rule_ids: list[str] = []
        # Primero entran todas las reglas que respaldan relaciones causales.
        # Después se completa con reglas descriptivas de cada mecánica.
        for node in mechanic_nodes:
            for rule_id in [
                relation["rule_id"] for relation in node.get("relations", [])
            ]:
                if rule_id not in prioritized_rule_ids:
                    prioritized_rule_ids.append(rule_id)
        for node in mechanic_nodes:
            for rule_id in node.get("rule_ids", []):
                if rule_id not in prioritized_rule_ids:
                    prioritized_rule_ids.append(rule_id)
        prioritized_rule_ids = prioritized_rule_ids[:MAX_RULES]
        rule_nodes = [
            self.nodes[f"rule:{rule_id}"]
            for rule_id in prioritized_rule_ids
            if f"rule:{rule_id}" in self.nodes
        ]
        if not rule_nodes:
            return None

        evidence: dict[str, dict] = {}
        for node in card_nodes:
            evidence[node["card_id"]] = {
                "id": node["card_id"],
                "kind": "card",
                "title": node["name"],
                "source": "knowledge_graph",
                "text": node["text"][:600],
            }
        for node in rule_nodes:
            evidence[node["rule_id"]] = {
                "id": node["rule_id"],
                "kind": "rule",
                "title": f"Regla {node['rule_id']}",
                "source": "knowledge_graph",
                "text": node["text"][:600],
            }

        context = self._format_context(
            query, card_nodes, mechanic_nodes, relations, rule_nodes
        )
        return {
            "card_ids": [node["card_id"] for node in card_nodes],
            "mechanics": selected_ids,
            "relations": relations,
            "evidence": evidence,
            "context": context,
            "context_chars": len(context),
            "coverage": "full",
        }

    def _format_context(
        self,
        query: str,
        card_nodes: list[dict],
        mechanic_nodes: list[dict],
        relations: list[dict],
        rule_nodes: list[dict],
    ) -> str:
        parts = [
            "INTERACCIÓN CUBIERTA POR EL GRAFO DE CONOCIMIENTO.",
            "Los hechos y relaciones siguientes son restricciones obligatorias.",
            "",
            "CARTAS EXACTAS:",
        ]
        for node in card_nodes:
            parts.append(
                f"[{node['card_id']}] {node['name']}: {node['text'][:700]}"
            )
        parts.extend(["", "HECHOS MECÁNICOS:"])
        for node in mechanic_nodes:
            for fact in node.get("facts", []):
                parts.append(f"- {node['title']}: {fact}")
        parts.extend(["", "RELACIONES CAUSALES:"])
        for relation in relations:
            parts.append(
                f"- {relation['label']} [regla {relation['rule_id']}]"
            )
        parts.extend(["", "EVIDENCIA EXACTA:"])
        for node in rule_nodes:
            # Las subreglas profundas suelen contener el ejemplo que decide la
            # interacción (p. ej. 359.3.e.14.b cita Deathgrip literalmente).
            limit = 1000 if node["rule_id"].count(".") >= 3 else 350
            parts.append(f"[{node['rule_id']}] {node['text'][:limit]}")
        parts.extend(["", f"PREGUNTA: {query}"])
        return "\n".join(parts)


GRAPH_SYSTEM_PROMPT = """Sos un juez de Riftbound que resuelve una interacción usando un grafo validado.
Respondé exclusivamente JSON válido, sin Markdown, con esta forma:
{
  "verdict": "SI|NO|RESUELTO|DEPENDE|INFORMATIVO|NO_RESUELTO",
  "supported": true,
  "confidence": "ALTA|MEDIA|BAJA",
  "challenge": "posible interpretación contraria y por qué falla o prevalece",
  "explanation": "respuesta directa en español y secuencia temporal breve",
  "citations": ["IDs exactos presentes entre corchetes"],
  "missing_info": "",
  "missing_rules_query": ""
}

Reglas:
- Usá únicamente las cartas, hechos, relaciones y reglas del contexto.
- Las RELACIONES CAUSALES son obligatorias: no inviertas su orden.
- El resolvedor solo usa este prompt cuando verificó cobertura completa. Si una regla
  oficial incluye un ejemplo con las mismas cartas, aplicalo directamente: ese ejemplo
  es evidencia suficiente y debe producir supported=true y confianza ALTA.
- Trigger no significa resolve.
- Verificá primero la legalidad de cada jugada.
- Para una interacción entre cartas, citá las cartas y al menos una regla.
- Usá NO_RESUELTO únicamente si falta un dato material del estado de juego. No te
  abstengas si una regla o ejemplo oficial del contexto resuelve exactamente el caso.
- Sé breve: respuesta directa y luego el orden de eventos relevante."""
