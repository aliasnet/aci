"""Tests for migrate_to_jsonl helpers."""

import json
import unittest

from entities.agi.agi_tools.migrate_to_jsonl import migrate


class NormalizeTimestampTests(unittest.TestCase):
    def test_preserves_existing_z_suffix(self) -> None:
        message = {"timestamp": "2023-05-05T12:34:56Z"}
        self.assertEqual(
            migrate.normalize_timestamp(message),
            "2023-05-05T12:34:56Z",
        )

    def test_normalizes_space_separated_z_timestamp(self) -> None:
        message = {"timestamp": "2023-05-05 15:00:00Z"}
        self.assertEqual(
            migrate.normalize_timestamp(message),
            "2023-05-05T15:00:00Z",
        )

    def test_converts_offset_to_utc(self) -> None:
        message = {"timestamp": "2023-05-05T12:34:56+02:00"}
        self.assertEqual(
            migrate.normalize_timestamp(message),
            "2023-05-05T10:34:56Z",
        )

    def test_converts_compact_offset_to_utc(self) -> None:
        message = {"timestamp": "2023-05-05T12:34:56+0200"}
        self.assertEqual(
            migrate.normalize_timestamp(message),
            "2023-05-05T10:34:56Z",
        )

    def test_converts_hour_only_offset_to_utc(self) -> None:
        message = {"timestamp": "2023-05-05T12:34:56+02"}
        self.assertEqual(
            migrate.normalize_timestamp(message),
            "2023-05-05T10:34:56Z",
        )

    def test_invalid_timestamp_raises(self) -> None:
        message = {"timestamp": "not-a-date"}
        with self.assertRaises(migrate.MigrationError):
            migrate.normalize_timestamp(message)

    def test_naive_timestamp_assumed_utc(self) -> None:
        naive_message = {"timestamp": "2023-05-05T12:34:56"}
        self.assertEqual(
            migrate.normalize_timestamp(naive_message),
            "2023-05-05T12:34:56Z",
        )


class CLISmokeTests(unittest.TestCase):
    def test_invalid_timestamp_results_in_error(self) -> None:
        data = {
            "messages": [
                {
                    "entity": "tester",
                    "role": "tester",
                    "content": "example",
                    "metadata": {},
                    "timestamp": "bad-value",
                }
            ]
        }
        input_path = migrate.ROOT / "tmp_test_invalid_timestamp.json"
        output_dir = migrate.ROOT / "tmp_output"
        try:
            input_path.write_text(json.dumps(data), encoding="utf-8")
            result = migrate.main(
                [
                    "--input",
                    str(input_path),
                    "--output-dir",
                    str(output_dir),
                    "--identity",
                    str(migrate.IDENTITY_FILE),
                    "--policy",
                    str(migrate.POLICY_FILE),
                ]
            )
        finally:
            if input_path.exists():
                input_path.unlink()
            if output_dir.exists():
                for child in output_dir.rglob("*"):
                    if child.is_file():
                        child.unlink()
                for child in sorted(output_dir.rglob("*"), reverse=True):
                    if child.is_dir():
                        child.rmdir()
                if output_dir.exists():
                    output_dir.rmdir()
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
