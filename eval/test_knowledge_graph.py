"""Pruebas sin API para integridad, cobertura y tamaño del contexto del grafo."""

import json
import sys
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from build_knowledge_graph import build_graph, validate_graph  # noqa: E402
from knowledge_resolver import KnowledgeResolver  # noqa: E402


class KnowledgeGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = json.loads((BASE_DIR / "cards.json").read_text(encoding="utf-8"))
        cls.cards_by_number = {
            card.get("card_number"): card
            for card in cls.cards
            if card.get("card_number")
        }
        cls.cases = json.loads(
            (BASE_DIR / "eval" / "judge_cases.json").read_text(encoding="utf-8")
        )
        cls.resolver = KnowledgeResolver(
            BASE_DIR / "knowledge" / "knowledge_graph.json"
        )

    def test_generated_graph_is_valid(self):
        report = validate_graph(build_graph())
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["stats"]["node_kinds"]["card"], 960)
        self.assertFalse(report["warnings"])

    def test_graph_cases_have_exact_coverage(self):
        for case in (case for case in self.cases if case.get("graph")):
            with self.subTest(case=case["id"]):
                resolution = self.resolver.resolve(
                    case["question"],
                    [self.cards_by_number[card_id] for card_id in case["cards"]],
                )
                self.assertIsNotNone(resolution)
                self.assertEqual(resolution["coverage"], "full")
                self.assertLess(resolution["context_chars"], 6000)
                evidence_text = " ".join(resolution["evidence"])
                for requirement in case["must_mention"]:
                    options = requirement if isinstance(requirement, list) else [requirement]
                    self.assertTrue(
                        any(option in evidence_text for option in options),
                        f"Caso {case['id']} sin evidencia {options}",
                    )

    def test_single_card_uses_rag_fallback(self):
        deathgrip = self.cards_by_number["SFD-163"]
        resolution = self.resolver.resolve("¿Qué hace Deathgrip?", [deathgrip])
        self.assertIsNone(resolution)

    def test_every_edge_has_provenance_and_existing_endpoints(self):
        graph = json.loads(
            (BASE_DIR / "knowledge" / "knowledge_graph.json").read_text(
                encoding="utf-8"
            )
        )
        node_ids = {node["id"] for node in graph["nodes"]}
        for item in graph["edges"]:
            self.assertIn(item["source"], node_ids)
            self.assertIn(item["target"], node_ids)
            self.assertTrue(item["provenance"]["source"])
            self.assertTrue(item["provenance"]["locator"])
            self.assertTrue(item["provenance"]["evidence"])


if __name__ == "__main__":
    unittest.main()
