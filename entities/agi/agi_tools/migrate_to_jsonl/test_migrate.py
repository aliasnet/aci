"""Tests for the JSON-based migrate_to_jsonl tool manifest."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "migrate_to_jsonl.json"
AGI_CONFIG_PATH = Path(__file__).resolve().parents[2] / "agi.json"
ARCHIVED_MODULE_PATH = Path(__file__).resolve().parent / "archive" / "migrate.py"


class MigrateToJsonlManifestTests(unittest.TestCase):
    def setUp(self) -> None:  # pragma: no cover - simple data load
        with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
            self.manifest = json.load(handle)

    def test_manifest_declares_pipeline_metadata(self) -> None:
        self.assertEqual(self.manifest["version"], "1.0")
        self.assertEqual(self.manifest["pipeline"], "agi.memory.migrate_to_jsonl")
        self.assertIn("Migrate legacy HiveMind exports", self.manifest["description"])

    def test_manifest_defines_inline_helper_pipelines(self) -> None:
        helper_names = [
            "migrate.collect_messages",
            "migrate.normalize_messages",
            "migrate.apply_filters",
            "migrate.apply_audit_requirements",
            "migrate.write_jsonl",
            "migrate.write_checksum",
            "migrate.append_ledger",
        ]
        pipelines = self.manifest.get("pipelines", {})
        def _contains_instruction(value: object) -> bool:
            if isinstance(value, dict):
                if any(key in value for key in ("instructions", "notes")):
                    return True
                return any(_contains_instruction(v) for v in value.values())
            if isinstance(value, list):
                return any(_contains_instruction(item) for item in value)
            return False

        for name in helper_names:
            self.assertIn(name, pipelines, f"{name} pipeline should be defined inline")
            steps = pipelines[name].get("steps", [])
            self.assertGreater(len(steps), 0, f"{name} pipeline should declare at least one step")
            instruction_found = any(_contains_instruction(step.get("map")) for step in steps)
            self.assertTrue(
                instruction_found,
                f"{name} pipeline should document its LLM execution instructions",
            )
        filter_pipeline = pipelines["migrate.apply_filters"]
        serialized = json.dumps(filter_pipeline)
        for keyword in ("allow_topics", "deny_tags", "drop_if_topic_missing"):
            self.assertIn(keyword, serialized)

    def test_manifest_sequences_checksum_and_ledger(self) -> None:
        calls = [step["call"] for step in self.manifest["steps"]]
        self.assertIn("migrate.write_checksum", calls)
        self.assertIn("migrate.append_ledger", calls)
        checksum_index = calls.index("migrate.write_checksum")
        ledger_index = calls.index("migrate.append_ledger")
        self.assertLess(checksum_index, ledger_index, "Checksum must be computed before ledger append")


class AgiConfigIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:  # pragma: no cover - simple data load
        with AGI_CONFIG_PATH.open("r", encoding="utf-8") as handle:
            self.agi_config = json.load(handle)

    def test_pipeline_reference_points_to_manifest(self) -> None:
        pipelines = self.agi_config.get("pipelines", {})
        self.assertIn("agi.memory.migrate_to_jsonl", pipelines)
        spec = pipelines["agi.memory.migrate_to_jsonl"]
        self.assertEqual(spec["spec_ref"], "entities/agi/agi_tools/migrate_to_jsonl.json")
        self.assertIn("raw_url", spec)


class MigrationModuleRetiredTests(unittest.TestCase):
    def test_python_module_archived(self) -> None:
        legacy_path = Path(__file__).resolve().with_name("migrate.py")
        self.assertFalse(legacy_path.exists(), "Legacy migrate.py should be archived, not active in module root")
        self.assertTrue(
            ARCHIVED_MODULE_PATH.exists(),
            "Archived migrate.py should still be available for historical reference",
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
