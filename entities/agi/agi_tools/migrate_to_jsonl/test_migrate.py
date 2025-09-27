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

    def test_manifest_includes_filter_step(self) -> None:
        steps = self.manifest["steps"]
        self.assertTrue(any(step["call"] == "migrate.apply_filters" for step in steps))
        filter_step = next(step for step in steps if step["call"] == "migrate.apply_filters")
        serialized = json.dumps(filter_step)
        self.assertIn("allow_topics", serialized)
        self.assertIn("deny_tags", serialized)
        self.assertIn("drop_if_topic_missing", serialized)
        self.assertIn("default_topic", serialized)

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
