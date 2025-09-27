"""Tests for the JSON-based migrate_to_jsonl tool manifest."""

from __future__ import annotations

import datetime as dt
import json
import importlib.util
from pathlib import Path
import unittest


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "migrate_to_jsonl.json"
AGI_CONFIG_PATH = Path(__file__).resolve().parents[2] / "agi.json"
ARCHIVED_MODULE_PATH = Path(__file__).resolve().parent / "archive" / "migrate.py"
EXPORT_POLICY_PATH = Path(__file__).resolve().parents[2] / "agi_export_policy.json"


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

    def test_manifest_policy_default_is_repo_relative(self) -> None:
        steps = self.manifest["steps"]
        policy_step = next(
            step
            for step in steps
            if step["call"] == "_args.get" and step["map"].get("key") == "policy"
        )
        default_path = policy_step["map"].get("default")
        self.assertEqual(default_path, "entities/agi/agi_export_policy.json")
        self.assertFalse(default_path.startswith("/"), "policy default should be repo-relative")

    def test_manifest_exposes_artifact_path_for_checksum(self) -> None:
        steps = self.manifest["steps"]
        write_step = next(step for step in steps if step["call"] == "migrate.write_jsonl")
        write_map = write_step["map"]
        self.assertIn("path_template", write_map)
        self.assertIn("filename_template", write_map)
        self.assertIn("timestamp_format", write_map)

        checksum_step = next(step for step in steps if step["call"] == "migrate.write_checksum")
        checksum_map = checksum_step["map"]
        self.assertEqual(checksum_map["path"], "$steps.9.value.path")
        self.assertEqual(checksum_map["artifact"], "$steps.9.value")

        ledger_step = next(step for step in steps if step["call"] == "migrate.append_ledger")
        self.assertEqual(ledger_step["map"]["artifact"], "$steps.9.value")

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


class ExportPolicyPathTests(unittest.TestCase):
    def test_identity_source_is_repo_relative(self) -> None:
        with EXPORT_POLICY_PATH.open("r", encoding="utf-8") as handle:
            policy = json.load(handle)

        identity_source = policy["agi_memory"]["identity_source"]
        self.assertEqual(identity_source, "entities/agi/agi_identity_manager.json")
        self.assertFalse(identity_source.startswith("/"), "identity_source must remain repo-relative")

    def test_filename_template_adopts_json_suffix_and_slug(self) -> None:
        with EXPORT_POLICY_PATH.open("r", encoding="utf-8") as handle:
            policy = json.load(handle)

        template = policy["agi_memory"]["filename_template"]
        self.assertTrue(template.endswith(".json"))
        self.assertIn("{summary_slug}", template)


class ArchivedMigratorPathResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location(
            "archived_migrate", str(ARCHIVED_MODULE_PATH)
        )
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        cls.module = module

    def test_resolve_path_accepts_repo_relative_identity(self) -> None:
        module = self.module
        relative_identity = Path("entities/agi/agi_identity_manager.json")
        resolved = module.resolve_path(relative_identity)
        expected = (module.get_repo_root() / relative_identity).resolve()
        self.assertEqual(resolved, expected)

    def test_resolve_path_translates_root_absolute_identity(self) -> None:
        module = self.module
        absolute_identity = Path("/entities/agi/agi_identity_manager.json")
        resolved = module.resolve_path(absolute_identity)
        expected = (module.get_repo_root() / "entities/agi/agi_identity_manager.json").resolve()
        self.assertEqual(resolved, expected)

    def test_resolve_path_translates_nested_absolute_identity(self) -> None:
        module = self.module
        absolute_identity = Path(
            "/opt/misc/workdir/entities/agi/agi_identity_manager.json"
        )
        resolved = module.resolve_path(absolute_identity)
        expected = (module.get_repo_root() / "entities/agi/agi_identity_manager.json").resolve()
        self.assertEqual(resolved, expected)

    def test_generate_filename_handles_optional_slug(self) -> None:
        module = self.module
        timestamp = dt.datetime(2024, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc)
        template = "{identity_lower}_agi_memory{summary_slug}_{timestamp}.json"
        filename = module.generate_filename(
            "AGI",
            timestamp,
            template,
            "%Y%m%dT%H%M%SZ",
            summary="Launch Review",
        )
        self.assertEqual(filename, "agi_agi_memory_launch_review_20241231T235959Z.json")

    def test_generate_filename_sanitizes_problematic_summary(self) -> None:
        module = self.module
        timestamp = dt.datetime(2024, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc)
        template = "{identity_lower}_agi_memory{summary_slug}_{timestamp}.json"
        filename = module.generate_filename(
            "AGI",
            timestamp,
            template,
            "%Y%m%dT%H%M%SZ",
            summary="  🚀 Mission: Launch/Review  ",
        )
        self.assertEqual(filename, "agi_agi_memory_mission_launch_review_20241231T235959Z.json")

    def test_generate_filename_omits_slug_when_empty(self) -> None:
        module = self.module
        timestamp = dt.datetime(2024, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc)
        template = "{identity_lower}_agi_memory{summary_slug}_{timestamp}.json"
        filename = module.generate_filename(
            "AGI",
            timestamp,
            template,
            "%Y%m%dT%H%M%SZ",
            summary="!!!",
        )
        self.assertEqual(filename, "agi_agi_memory_20241231T235959Z.json")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
