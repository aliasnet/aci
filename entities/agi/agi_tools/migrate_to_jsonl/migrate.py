#!/usr/bin/env python3
# Lightweight migrator: reads identity/policy, enforces filters, normalizes ts, orders events, injects export event.

import argparse
import datetime
import json
import os
from datetime import timezone
from pathlib import Path


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


DEFAULT_REPO_ROOT = Path("/workspace/aci")


def detect_repo_root() -> Path:
    """Return the repository root, defaulting to /workspace/aci."""

    env_root = os.environ.get("ACI_REPO_ROOT")
    if env_root:
        return Path(env_root).resolve()

    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".git").exists() or (parent / "prime_directive.txt").exists():
            return parent
    return DEFAULT_REPO_ROOT


REPO_ROOT = detect_repo_root()


def resolve_path(base_file: Path, maybe_path: str) -> Path:
    """Resolve a path relative to the policy file and repository root."""

    base_dir = Path(base_file).parent if base_file else REPO_ROOT
    candidate = Path(maybe_path)
    probes = []

    if candidate.is_absolute():
        probes.append(candidate)
        try:
            probes.append(REPO_ROOT / candidate.relative_to("/"))
        except ValueError:
            # Non-rooted absolutes (e.g. Windows drives) are not expected; keep original.
            pass
    else:
        probes.append(base_dir / candidate)
        probes.append(REPO_ROOT / candidate)

    for path in probes:
        normalized = path.resolve()
        if normalized.exists():
            return normalized

    searched = ", ".join(str(p.resolve()) for p in probes)
    raise SystemExit(
        f"ERROR: Unable to resolve '{maybe_path}' relative to {base_file}. Checked: {searched}"
    )


def normalize_ts(ts: str) -> str:
    """Normalize timestamps to strict RFC 3339 UTC (..Z) form."""

    if ts.endswith("Z"):
        # Validate the format to catch malformed values such as missing date/time parts.
        try:
            datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError as exc:  # pragma: no cover - defensive guard
            raise SystemExit(f"ERROR: Invalid timestamp format: {ts}") from exc
        return ts

    try:
        dt = datetime.datetime.fromisoformat(ts)
    except ValueError as exc:
        raise SystemExit(f"ERROR: Invalid timestamp format: {ts}") from exc

    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc)
    else:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.isoformat().replace("+00:00", "Z")


def select_identity(identity_manager, cli_key=None):
    if cli_key:
        return cli_key
    active = identity_manager.get("active")
    if active:
        return active
    # legacy: try identity with default=true
    for ident, meta in identity_manager.get("agi_identities", {}).items():
        if meta.get("default") is True:
            return ident
    raise SystemExit("ERROR: No --identity-key provided and no active/default identity configured.")


def topic_allowed(event, filters):
    allow = set(filters.get("allow_topics", []))
    if not allow:
        return True
    t = event.get("type")
    if not t:
        return not filters.get("drop_if_topic_missing", False)
    return t in allow


def tags_denied(event, filters):
    deny = set(filters.get("deny_tags", []))
    tags = set(event.get("tags", []))
    return any(tag in deny for tag in tags)


def apply_filters(events, filters):
    out = []
    default_topic = filters.get("default_topic")
    for e in events:
        if not e.get("type") and default_topic:
            e["type"] = default_topic
        if not topic_allowed(e, filters):
            continue
        if tags_denied(e, filters):
            continue
        out.append(e)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy-file", required=True)
    ap.add_argument("--identity-source", required=False)
    ap.add_argument("--identity-key", required=False)
    ap.add_argument("--in", dest="inp", required=True, help="input ndjson/jsonl")
    ap.add_argument("--out", dest="out", required=True, help="output jsonl path")
    args = ap.parse_args()

    policy_file = Path(args.policy_file)
    policy = load_json(policy_file)["agi_memory"]
    identity_source = args.identity_source or policy.get("identity_source")
    if not identity_source:
        raise SystemExit("ERROR: No identity_source configured in policy or CLI args.")

    identity_source_path = resolve_path(policy_file, identity_source)
    ident_mgr = load_json(identity_source_path)
    identity_key = select_identity(ident_mgr, args.identity_key)

    raw = [json.loads(line) for line in Path(args.inp).read_text(encoding="utf-8").splitlines() if line.strip()]

    # normalize timestamps, enforce schema
    schema = policy.get("schema", "hivemind_agi_memory")
    for e in raw:
        if "schema" not in e:
            e["schema"] = schema
        if "actor" not in e:
            e["actor"] = "agi"
        if "ts" in e:
            e["ts"] = normalize_ts(e["ts"])

    # filters
    filtered = apply_filters(raw, policy.get("filters", {}))

    # chronological order
    filtered.sort(key=lambda e: e.get("ts", ""))

    # inject export event
    nowz = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    export_evt = {
        "schema": schema,
        "type": "export",
        "ts": nowz,
        "actor": "system",
        "summary": "Migrator exported AGI memory",
        "data": {},
        "tags": ["export", "cli", "audit", "identity:" + identity_key],
    }
    filtered.append(export_evt)

    # write jsonl
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        for e in filtered:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
