# Task Queue

This directory contains machine-readable task definitions that replace the informal log entries in `issues.md`.

Each task document includes:
- metadata identifying when the task was opened and which branch spawned it
- explicit acceptance criteria and dependency ordering
- branch and patch instructions so the work can be replayed on a clean head

Once a task is completed, update its `status` and append the outcome to `issues.md` per the append-only policy.
