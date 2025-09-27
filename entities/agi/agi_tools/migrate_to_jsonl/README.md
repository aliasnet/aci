# AGI Memory Migrator (JSON Manifest)

The legacy Python migrator is now archived under `archive/migrate.py`. Active migrations are orchestrated by the JSON manifest at
`entities/agi/agi_tools/migrate_to_jsonl.json`, which can be invoked by automation or CLI wrappers.

## Usage

```bash
aci memory migrate --input <legacy_export.json> --output-dir memory/agi_memory/AGI
```

The manifest-driven workflow performs the following high-level steps:

1. Resolve CLI arguments (`--input`, `--output-dir`, optional `--identity`, optional `--policy`).
2. Load `agi_export_policy.json` and the referenced `agi_identity_manager.json` to bind the correct identity metadata.
3. Parse the legacy payload, normalize timestamps and message metadata, and enforce governance filters (`allow_topics`, `deny_tags`,
   `drop_if_topic_missing`, `default_topic`).
4. Apply policy audit requirements (chronological ordering, export audit injection, optional ledger append).
5. Write the normalized JSONL artifact alongside a SHA-256 checksum file in the requested output directory.

For detailed step definitions see the manifest itself. The archived Python utility can be referenced for historical behavior but is
no longer executed directly.
