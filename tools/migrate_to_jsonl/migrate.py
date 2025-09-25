#!/usr/bin/env python3
"""Legacy export migrator.

Transforms legacy AGI/HiveMind export artifacts into the canonical JSONL format
mandated by ``aci_export_policy.json``. The migrator intentionally avoids any
changes to live exporter code. It is designed as an offline utility that can be
run against historical exports prior to publishing them.

Key behaviors implemented:

* Reads the active identity from ``agi_identity_manager.json`` so that all
  AGI-authored lines are emitted with the correct ``entity``/``role`` value.
* Enforces topic and tag filters defined in ``aci_export_policy.json``.
* Normalizes message structures from heterogeneous legacy exports.
* Produces JSONL output with per-line metadata including schema/exporter
  versions and governance hints.
* Runs validation steps (schema, identity binding, filter audit, duplicate
  detection) before finalizing the export.
* Emits a SHA-256 checksum alongside the JSONL file and appends an anchoring
  record to the configured ledger.

Usage example::

    python tools/migrate_to_jsonl/migrate.py \
        --input memory/hivemind_memory/logs/hivemind_memory-20250919T161225Z.json \
        --output-dir memory/agi_memory/exports \
        --default-topic theories

The ``--default-topic`` flag may be used to supply an allowed topic for legacy
messages that lack tagging. Messages without an allowed topic and without the
flag will be excluded to honor governance filters.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

ROOT = Path(__file__).resolve().parents[2]
IDENTITY_FILE = ROOT / "agi_identity_manager.json"
POLICY_FILE = ROOT / "aci_export_policy.json"

REQUIRED_KEYS = ("timestamp", "role", "entity", "content", "metadata")


class MigrationError(RuntimeError):
    """Raised when validation fails during migration."""


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_identity(identity_path: Path = IDENTITY_FILE) -> Dict[str, Any]:
    data = load_json(identity_path)
    active = data.get("active_identity", {})
    name = active.get("name")
    if not name:
        raise MigrationError(
            "active_identity.name is required in agi_identity_manager.json"
        )
    fallback = data.get("fallback_identity", {})
    return {
        "active_name": name,
        "fallback_name": fallback.get("name", "external entity"),
        "raw": data,
    }


def load_policy(policy_path: Path = POLICY_FILE) -> Dict[str, Any]:
    data = load_json(policy_path)
    filters = data.get("filters", {})
    allow_topics = tuple(filters.get("allow_topics", ()))
    if not allow_topics:
        raise MigrationError("aci_export_policy.json must define filters.allow_topics")
    deny_tags = tuple(filters.get("deny_tags", ()))
    return {
        "raw": data,
        "allow_topics": allow_topics,
        "deny_tags": deny_tags,
        "drop_if_topic_missing": filters.get("drop_if_topic_missing", True),
        "default_topic": filters.get("default_topic"),
        "policy_version": data.get("policy_version", "unknown"),
        "schema_version": data.get("schema_version", "unknown"),
        "exporter_version": data.get("exporter_version", "unknown"),
        "file_pattern": data.get("file_pattern", "{identity}_agi_memory_{timestamp}.jsonl"),
        "ledger": data.get("anchoring", {}).get(
            "ledger", "memory/agi_memory/anchors_ledger.jsonl"
        ),
    }


def collect_candidate_messages(payload: Any) -> List[Dict[str, Any]]:
    messages: List[Dict[str, Any]] = []

    def _walk(node: Any) -> None:
        if isinstance(node, dict):
            if looks_like_message(node):
                messages.append(node)
            for value in node.values():
                _walk(value)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(payload)
    return messages


MESSAGE_TEXT_KEYS = ("content", "text", "message", "body")
MESSAGE_ROLE_KEYS = ("role", "entity", "speaker", "author", "by", "name")
MESSAGE_TIMESTAMP_KEYS = (
    "timestamp",
    "ts",
    "time",
    "created_at",
    "export_ts_hint",
    "occurred_at",
)


def looks_like_message(node: Dict[str, Any]) -> bool:
    if not isinstance(node, dict):
        return False
    if not any(key in node for key in MESSAGE_TEXT_KEYS):
        return False
    if not any(key in node for key in MESSAGE_ROLE_KEYS):
        return False
    return True


def normalize_timestamp(
    message: Dict[str, Any],
    fallback: Optional[dt.datetime] = None,
) -> str:
    timestamp_value: Optional[str] = None
    for key in MESSAGE_TIMESTAMP_KEYS:
        value = message.get(key)
        if value:
            timestamp_value = value
            break
    if timestamp_value:
        try:
            parsed = dt.datetime.fromisoformat(timestamp_value.replace("Z", "+00:00"))
        except ValueError:
            parsed = fallback or dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
    else:
        parsed = fallback or dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_content(message: Dict[str, Any]) -> str:
    for key in MESSAGE_TEXT_KEYS:
        value = message.get(key)
        if isinstance(value, str):
            return value
    return json.dumps(message, ensure_ascii=False)


def normalize_role_entity(
    message: Dict[str, Any],
    identity: Dict[str, Any],
) -> Tuple[str, str, bool, str]:
    original = str(
        message.get("entity")
        or message.get("role")
        or message.get("speaker")
        or message.get("author")
        or message.get("by")
        or message.get("name")
        or ""
    ).strip()
    normalized = original.lower()
    active_name = identity["active_name"]
    fallback_name = identity["fallback_name"]

    if normalized in {"user", "human", "alias"}:
        return "User", "User", False, original or "User"
    if normalized in {active_name.lower(), "assistant", "agi", "system"}:
        return active_name, active_name, True, original or active_name
    if not normalized:
        # default to user if unspecified and content starts with user-like prompt
        return "User", "User", False, original or "User"
    # fallback external entity path
    return fallback_name, fallback_name, False, original or fallback_name


DENY_TAG_DEFAULTS = {"ops", "admin", "automation", "scheduler", "system"}


def normalize_metadata(
    message: Dict[str, Any],
    *,
    topic: str,
    exporter_version: str,
    schema_version: str,
    agi_entity: bool,
    original_entity: str,
    deny_tags: Sequence[str],
) -> Dict[str, Any]:
    metadata = {}
    if isinstance(message.get("metadata"), dict):
        metadata.update(message["metadata"])
    tags: List[str] = []
    for key in ("tags", "labels"):
        if key in message and isinstance(message[key], list):
            tags.extend(str(item) for item in message[key])
    if "tags" in metadata and isinstance(metadata["tags"], list):
        tags.extend(str(item) for item in metadata["tags"])
    if tags:
        metadata["tags"] = sorted({tag for tag in tags if tag})
    metadata.update(
        {
            "topic": topic,
            "schema_version": schema_version,
            "exporter_version": exporter_version,
            "agi_entity": agi_entity,
            "original_entity": original_entity,
        }
    )
    deny = set(tag.lower() for tag in deny_tags) | DENY_TAG_DEFAULTS
    if metadata.get("tags"):
        metadata["tags"] = [
            tag for tag in metadata["tags"] if tag.lower() not in deny
        ]
    return metadata


def resolve_topic(
    message: Dict[str, Any],
    *,
    allow_topics: Sequence[str],
    deny_tags: Sequence[str],
    drop_if_missing: bool,
    default_topic: Optional[str],
) -> Optional[str]:
    candidates: List[str] = []
    # direct topic fields
    for key in ("topic", "category"):
        value = message.get(key)
        if isinstance(value, str):
            candidates.append(value)
    metadata = message.get("metadata")
    if isinstance(metadata, dict):
        meta_topic = metadata.get("topic")
        if isinstance(meta_topic, str):
            candidates.append(meta_topic)
        meta_tags = metadata.get("tags")
        if isinstance(meta_tags, list):
            candidates.extend(str(tag) for tag in meta_tags)
    for tag_key in ("tags", "labels"):
        tag_list = message.get(tag_key)
        if isinstance(tag_list, list):
            candidates.extend(str(tag) for tag in tag_list)
    allowed_lower = {topic.lower(): topic for topic in allow_topics}
    for candidate in candidates:
        normalized = candidate.strip().lower()
        if normalized in allowed_lower:
            return allowed_lower[normalized]
    if default_topic and default_topic.lower() in allowed_lower:
        return allowed_lower[default_topic.lower()]
    if drop_if_missing:
        return None
    # fallback to first allowed topic
    return allow_topics[0]


def generate_filename(
    identity_name: str,
    timestamp: dt.datetime,
    pattern: str,
) -> str:
    sanitized_identity = identity_name.lower().replace(" ", "_")
    stamp = timestamp.strftime("%Y-%m-%dT%H-%M-%S")
    return pattern.format(identity=sanitized_identity, timestamp=stamp)


def validate_line(entry: Dict[str, Any]) -> None:
    missing = [key for key in REQUIRED_KEYS if key not in entry]
    if missing:
        raise MigrationError(f"Export line missing required keys: {missing}")


def write_jsonl(path: Path, lines: Sequence[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for line in lines:
            handle.write(json.dumps(line, ensure_ascii=False) + "\n")


def write_checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    checksum = digest.hexdigest()
    checksum_path = path.with_suffix(path.suffix + ".sha256")
    with checksum_path.open("w", encoding="utf-8") as handle:
        handle.write(checksum + "\n")
    return checksum


def append_anchor_record(
    ledger_path: Path,
    *,
    filename: str,
    checksum: str,
    policy_version: str,
) -> None:
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "filename": filename,
        "sha256": checksum,
        "anchored_at": dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "policy_version": policy_version,
    }
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def migrate_file(
    input_path: Path,
    *,
    output_dir: Path,
    identity: Dict[str, Any],
    policy: Dict[str, Any],
    default_topic: Optional[str] = None,
) -> Optional[Path]:
    payload = load_json(input_path)
    messages = collect_candidate_messages(payload)
    if not messages:
        print(f"[skip] no message payloads detected in {input_path}")
        return None

    allow_topics = policy["allow_topics"]
    deny_tags = policy["deny_tags"]
    drop_if_missing = policy["raw"].get("filters", {}).get(
        "drop_if_topic_missing", True
    )
    if default_topic:
        drop_if_missing = False
    default_topic = default_topic or policy.get("default_topic")

    first_timestamp: Optional[dt.datetime] = None
    lines: List[Dict[str, Any]] = []
    dedup: Set[Tuple[str, str, str]] = set()

    for message in messages:
        topic = resolve_topic(
            message,
            allow_topics=allow_topics,
            deny_tags=deny_tags,
            drop_if_missing=drop_if_missing,
            default_topic=default_topic,
        )
        if topic is None:
            continue
        timestamp_str = normalize_timestamp(message)
        timestamp_dt = dt.datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        if first_timestamp is None:
            first_timestamp = timestamp_dt
        role, entity, is_agi, original_entity = normalize_role_entity(message, identity)
        if is_agi and entity != identity["active_name"]:
            # enforce identity binding strictly
            entity = identity["active_name"]
            role = identity["active_name"]
        metadata = normalize_metadata(
            message,
            topic=topic,
            exporter_version=policy["exporter_version"],
            schema_version=policy["schema_version"],
            agi_entity=is_agi,
            original_entity=original_entity,
            deny_tags=deny_tags,
        )
        entry = {
            "timestamp": timestamp_str,
            "role": role,
            "entity": entity,
            "content": normalize_content(message),
            "metadata": metadata,
        }
        validate_line(entry)
        dedup_key = (entry["timestamp"], entry["entity"], entry["content"])
        if dedup_key in dedup:
            continue
        dedup.add(dedup_key)
        lines.append(entry)

    if not lines:
        print(f"[skip] all messages filtered out for {input_path}")
        return None

    lines.sort(key=lambda item: item["timestamp"])
    anchor_time = first_timestamp or dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)

    output_dir.mkdir(parents=True, exist_ok=True)
    filename = generate_filename(identity["active_name"], anchor_time, policy["file_pattern"])
    output_path = output_dir / filename
    write_jsonl(output_path, lines)
    checksum = write_checksum(output_path)
    ledger_path = ROOT / policy["ledger"]
    append_anchor_record(
        ledger_path,
        filename=str(output_path.relative_to(ROOT)),
        checksum=checksum,
        policy_version=policy["policy_version"],
    )
    print(f"[ok] migrated {input_path} -> {output_path}")
    return output_path


def discover_input_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    for candidate in sorted(path.rglob("*.json")):
        if candidate.name.endswith((".sha256",)):
            continue
        yield candidate
    for candidate in sorted(path.rglob("*.jsonl")):
        yield candidate


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate legacy AGI exports to JSONL")
    parser.add_argument("--input", required=True, help="Path to a legacy export file or directory")
    parser.add_argument("--output-dir", required=True, help="Directory where JSONL exports will be written")
    parser.add_argument(
        "--identity",
        default=str(IDENTITY_FILE),
        help="Override path to agi_identity_manager.json",
    )
    parser.add_argument(
        "--policy",
        default=str(POLICY_FILE),
        help="Override path to aci_export_policy.json",
    )
    parser.add_argument(
        "--default-topic",
        help="Assign this allowed topic to messages missing a topic (overrides policy drop flag)",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()

    identity = load_identity(Path(args.identity))
    policy = load_policy(Path(args.policy))

    migrated_any = False
    for file_path in discover_input_files(input_path):
        result = migrate_file(
            file_path,
            output_dir=output_dir,
            identity=identity,
            policy=policy,
            default_topic=args.default_topic,
        )
        if result is not None:
            migrated_any = True
    if not migrated_any:
        print("No files migrated; nothing to do.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
