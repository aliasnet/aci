#!/usr/bin/env python3
"""Legacy export migrator.

Transforms legacy AGI/HiveMind export artifacts into the canonical JSONL format
mandated by ``agi_export_policy.json``. The migrator intentionally avoids any
changes to live exporter code. It is designed as an offline utility that can be
run against historical exports prior to publishing them.

Key behaviors implemented:

* Resolves identity metadata via ``agi_identity_manager.json`` (multiple
  identities may be defined; callers choose which identity key to bind).
* Normalizes message structures from heterogeneous legacy exports.
* Produces JSONL output with per-line metadata including schema/exporter
  versions and governance hints defined by the export policy.
* Runs validation steps (schema, identity binding, optional filtering, duplicate
  detection) before finalizing the export.
* Emits a SHA-256 checksum alongside the JSONL file and (optionally) appends an
  anchoring record to the configured ledger if the policy requests it.

Usage example::

    python entities/agi/agi_tools/migrate_to_jsonl/migrate.py \
        --input memory/hivemind_memory/logs/hivemind_memory-20250919T161225Z.json \
        --output-dir memory/agi_memory/exports \
        --default-topic theories

The ``--default-topic`` flag may be used to supply a topic for legacy messages
that lack tagging.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple, Union

DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[4]
ROOT = Path(__file__).resolve().parents[2]
IDENTITY_FILE = ROOT / "agi_identity_manager.json"
POLICY_FILE = ROOT / "agi_export_policy.json"

FILESYSTEM_ROOT = Path("/")

REQUIRED_KEYS = ("timestamp", "role", "identity", "content", "metadata")
LEGACY_IDENTITY_KEYS = (
    "entity",
    "actor",
    "speaker",
    "author",
    "by",
    "name",
    "role",
)


class MigrationError(RuntimeError):
    """Raised when validation fails during migration."""


def get_repo_root() -> Path:
    """Return the repository root, honoring ``ACI_REPO_ROOT`` overrides."""

    env_root = os.environ.get("ACI_REPO_ROOT")
    if not env_root:
        return DEFAULT_REPO_ROOT
    candidate = Path(env_root).expanduser()
    if not candidate.is_absolute():
        candidate = (DEFAULT_REPO_ROOT / candidate).resolve()
    return candidate


def resolve_path(
    reference: Union[str, Path], *, repo_root: Optional[Path] = None
) -> Path:
    """Resolve ``reference`` against the active repository root."""

    path = Path(reference).expanduser()
    base_root = repo_root or get_repo_root()

    if path.is_absolute():
        fallbacks: List[Path] = []

        try:
            relative = path.relative_to(base_root)
        except ValueError:
            relative = None
        if relative is not None:
            fallbacks.append(base_root / relative)

        if path.anchor == FILESYSTEM_ROOT.anchor and len(path.parts) > 1:
            known_anchors = {"entities", "memory", "library", "aig"}
            parts = path.parts
            for index, part in enumerate(parts):
                if part in known_anchors:
                    fallbacks.append(base_root / Path(*parts[index:]))
                    break

        for candidate in fallbacks:
            resolved_candidate = candidate.resolve()
            if resolved_candidate.exists():
                return resolved_candidate
        if fallbacks:
            return fallbacks[0].resolve()
        if path.exists():
            return path
        return path

    return (base_root / path).resolve()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_identity(
    identity_path: Path = IDENTITY_FILE,
    identity_key: Optional[str] = None,
) -> Dict[str, Any]:
    data = load_json(identity_path)
    identities = data.get("agi_identities", {})
    if not isinstance(identities, dict) or not identities:
        raise MigrationError("agi_identity_manager.json must define agi_identities")

    selected_key = identity_key
    entry: Optional[Dict[str, Any]] = None

    if selected_key:
        entry = identities.get(selected_key)
        if entry is None:
            raise MigrationError(
                f"Identity '{selected_key}' not found in agi_identity_manager.json"
            )

    if entry is None:
        # Prefer a concrete identity that declares a key.
        for candidate_key, candidate_entry in identities.items():
            if isinstance(candidate_entry, dict) and "key" in candidate_entry:
                entry = candidate_entry
                selected_key = candidate_key
                break

    if entry is None:
        # Fallback to the first declared identity.
        selected_key, entry = next(iter(identities.items()))
        if not isinstance(entry, dict):
            raise MigrationError(
                "Invalid identity entry in agi_identity_manager.json (expected object)"
            )

    active_name = entry.get("key") or selected_key
    fallback_entry = identities.get("agi-external")
    fallback_name = "external entity"
    if isinstance(fallback_entry, dict):
        fallback_name = (
            fallback_entry.get("key")
            or fallback_entry.get("role")
            or fallback_name
        )

    return {
        "active_name": str(active_name),
        "active_id": str(selected_key),
        "fallback_name": str(fallback_name),
        "raw": data,
    }


def load_policy(policy_path: Path = POLICY_FILE) -> Dict[str, Any]:
    data = load_json(policy_path)
    memory = data.get("agi_memory", {})
    if not isinstance(memory, dict):
        raise MigrationError("agi_export_policy.json must define agi_memory block")

    filename_template = memory.get(
        "filename_template", "{identity_lower}_agi_memory_{timestamp}.jsonl"
    )
    timestamp_format_hint = memory.get("timestamp_format", "Ymd-THMSZ")

    return {
        "raw": data,
        "allow_topics": tuple(memory.get("allow_topics", ())),
        "deny_tags": tuple(memory.get("deny_tags", ())),
        "drop_if_topic_missing": bool(memory.get("drop_if_topic_missing", False)),
        "default_topic": memory.get("default_topic"),
        "policy_version": data.get("version", "unknown"),
        "schema_version": memory.get("schema", "unknown"),
        "exporter_version": data.get("version", "unknown"),
        "filename_template": filename_template,
        "timestamp_format": translate_timestamp_format(timestamp_format_hint),
        "path_template": memory.get("path_template"),
        "identity_source": memory.get("identity_source"),
        "ledger": memory.get("audit", {}).get("ledger_path"),
        "audit": memory.get("audit", {}),
    }


def translate_timestamp_format(pattern: str) -> str:
    mapping = {
        "Y": "%Y",
        "m": "%m",
        "d": "%d",
        "H": "%H",
        "M": "%M",
        "S": "%S",
        "T": "T",
    }
    translated: List[str] = []
    for char in pattern:
        translated.append(mapping.get(char, char))
    return "".join(translated)


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
MESSAGE_ROLE_KEYS = ("identity", "actor", "role", "entity", "speaker", "author", "by", "name")
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


ISO8601_OFFSET_PATTERN = re.compile(
    r"^(?P<prefix>.*?)(?P<sign>[+-])(?P<hours>\d{2})(?::?(?P<minutes>\d{2})"
    r"(?::?(?P<seconds>\d{2}))?)?$"
)


def _coerce_iso8601(value: str) -> Tuple[str, bool]:
    """Return a string parseable by ``datetime.fromisoformat``.

    The second element of the tuple indicates whether the original string ended
    with a ``Z`` suffix.
    """

    cleaned = value.strip()
    if not cleaned:
        raise ValueError("empty timestamp string")

    had_z = cleaned.endswith("Z") or cleaned.endswith("z")
    candidate = cleaned

    if "T" not in candidate and " " in candidate:
        # Allow ``YYYY-MM-DD HH:MM:SS`` style strings.
        candidate = candidate.replace(" ", "T", 1)

    if had_z:
        candidate = candidate[:-1] + "+00:00"

    match = ISO8601_OFFSET_PATTERN.match(candidate)
    if match and ":" not in candidate[match.start("sign") :]:
        hours = match.group("hours")
        minutes = match.group("minutes") or "00"
        seconds = match.group("seconds")
        offset = f"{match.group('sign')}{hours}:{minutes}"
        if seconds:
            offset += f":{seconds}"
        candidate = f"{match.group('prefix')}{offset}"

    return candidate, had_z


def normalize_timestamp(
    message: Dict[str, Any],
    fallback: Optional[dt.datetime] = None,
) -> str:
    timestamp_value: Optional[str] = None
    for key in MESSAGE_TIMESTAMP_KEYS:
        value = message.get(key)
        if value:
            timestamp_value = str(value)
            break

    if timestamp_value:
        try:
            candidate, had_z = _coerce_iso8601(timestamp_value)
            parsed = dt.datetime.fromisoformat(candidate)
        except ValueError as exc:
            raise MigrationError(
                f"Invalid timestamp '{timestamp_value}' (expected ISO-8601 format)"
            ) from exc
    else:
        parsed = fallback or dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
        had_z = False

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)

    parsed_utc = parsed.astimezone(dt.timezone.utc)
    canonical = parsed_utc.isoformat().replace("+00:00", "Z")

    if timestamp_value and had_z:
        original = timestamp_value.strip()
        if original.endswith("z"):
            original = original[:-1] + "Z"
        if original == canonical:
            return original

    return canonical


def normalize_content(message: Dict[str, Any]) -> str:
    for key in MESSAGE_TEXT_KEYS:
        value = message.get(key)
        if isinstance(value, str):
            return value
    return json.dumps(message, ensure_ascii=False)


def normalize_role_identity(
    message: Dict[str, Any],
    identity: Dict[str, Any],
) -> Tuple[str, str, bool, str, Optional[str]]:
    original = ""
    source_key: Optional[str] = None
    for key in ("identity", "actor", "entity", "role", "speaker", "author", "by", "name"):
        value = message.get(key)
        if isinstance(value, str) and value.strip():
            original = value.strip()
            source_key = key
            break

    normalized = original.lower()
    active_name = identity["active_name"]
    fallback_name = identity["fallback_name"]

    if normalized in {"user", "human", "alias"}:
        return "User", "User", False, original or "User", source_key
    if normalized in {active_name.lower(), "assistant", "agi", "system"}:
        return active_name, active_name, True, original or active_name, source_key
    if not normalized:
        # default to user if unspecified and content starts with user-like prompt
        return "User", "User", False, original or "User", source_key
    # fallback external identity path
    return fallback_name, fallback_name, False, original or fallback_name, source_key


DENY_TAG_DEFAULTS = {"ops", "admin", "automation", "scheduler", "system"}


def normalize_metadata(
    message: Dict[str, Any],
    *,
    topic: str,
    exporter_version: str,
    schema_version: str,
    agi_entity: bool,
    original_identity: str,
    identity_source: Optional[str],
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
            "original_identity": original_identity,
        }
    )
    if identity_source and identity_source != "identity":
        metadata.setdefault("legacy_identity_key", identity_source)
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
    deny = {tag.lower() for tag in deny_tags}

    if allow_topics:
        for candidate in candidates:
            normalized = candidate.strip().lower()
            if normalized in allowed_lower and normalized not in deny:
                return allowed_lower[normalized]
        if default_topic and default_topic.lower() in allowed_lower:
            return allowed_lower[default_topic.lower()]
        if drop_if_missing:
            return None
        return allow_topics[0]

    for candidate in candidates:
        normalized = candidate.strip()
        if normalized and normalized.lower() not in deny:
            return normalized
    if default_topic:
        return default_topic
    return "general"


def generate_filename(
    identity_name: str,
    timestamp: dt.datetime,
    template: str,
    timestamp_format: str,
) -> str:
    normalized = identity_name.replace(" ", "_")
    context = {
        "identity": normalized,
        "identity_lower": normalized.lower(),
        "timestamp": timestamp.strftime(timestamp_format),
    }
    return template.format(**context)


def validate_line(entry: Dict[str, Any]) -> None:
    if "identity" not in entry:
        for legacy_key in LEGACY_IDENTITY_KEYS:
            if legacy_key in entry:
                legacy_value = entry[legacy_key]
                entry["identity"] = legacy_value

                if legacy_key not in REQUIRED_KEYS:
                    entry.pop(legacy_key)

                existing_metadata = entry.get("metadata", {})
                if isinstance(existing_metadata, dict):
                    metadata = existing_metadata
                else:
                    metadata = {"legacy_metadata": existing_metadata}
                metadata.setdefault("legacy_identity_key", legacy_key)
                entry["metadata"] = metadata
                break
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

    allow_topics = policy.get("allow_topics", ())
    deny_tags = policy.get("deny_tags", ())
    drop_if_missing = bool(policy.get("drop_if_topic_missing", False))
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
        try:
            timestamp_str = normalize_timestamp(message)
        except MigrationError as exc:
            raise MigrationError(f"{input_path}: {exc}") from exc
        timestamp_dt = dt.datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        if first_timestamp is None:
            first_timestamp = timestamp_dt
        (
            role,
            identity_name,
            is_agi,
            original_identity,
            identity_source,
        ) = normalize_role_identity(message, identity)
        if is_agi and identity_name != identity["active_name"]:
            # enforce identity binding strictly
            identity_name = identity["active_name"]
            role = identity["active_name"]
        metadata = normalize_metadata(
            message,
            topic=topic,
            exporter_version=policy["exporter_version"],
            schema_version=policy["schema_version"],
            agi_entity=is_agi,
            original_identity=original_identity,
            identity_source=identity_source,
            deny_tags=deny_tags,
        )
        entry = {
            "timestamp": timestamp_str,
            "role": role,
            "identity": identity_name,
            "content": normalize_content(message),
            "metadata": metadata,
        }
        validate_line(entry)
        dedup_key = (entry["timestamp"], entry["identity"], entry["content"])
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
    filename = generate_filename(
        identity["active_name"],
        anchor_time,
        policy["filename_template"],
        policy["timestamp_format"],
    )
    output_path = output_dir / filename
    write_jsonl(output_path, lines)
    checksum = write_checksum(output_path)
    ledger_path_value = policy.get("ledger")
    if ledger_path_value:
        ledger_path = ROOT / ledger_path_value
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
        "--identity-key",
        help="Identity key from agi_identity_manager.json to bind exports",
    )
    parser.add_argument(
        "--policy",
        default=str(POLICY_FILE),
        help="Override path to agi_export_policy.json",
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

    try:
        identity_path = resolve_path(args.identity)
        policy_path = resolve_path(args.policy)
        identity = load_identity(identity_path, args.identity_key)
        policy = load_policy(policy_path)

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
    except MigrationError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
