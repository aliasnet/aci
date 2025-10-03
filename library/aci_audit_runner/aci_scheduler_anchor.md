# ACI Scheduler Anchor — Human‑Readable Schedule Spec (v0.2)

**Purpose**
This single file describes (in natural language) *what to schedule*, *where the files live*, and *how to recover* if the environment is corrupted. Operators can paste this into any job scheduler (cron, systemd timers, Task Scheduler, Kubernetes, etc.) and follow it verbatim.

---

## 1) Canonical Locations (authoritative)

* **Runner (local stub/interpreter):** `/mnt/data/aci/library/aci_runner/adaptive_audit_runner.py`
* **JSON Spec (source of truth):** `/mnt/data/aci/config/aci_runner_spec.json`
* **Local fallback root:** `/mnt/data/aci/local/`
* **State snapshots:** `/mnt/data/aci/state/active.json`
* **Audit records (temp/quiet):** `/mnt/data/aci/audit/tmp/`
* **Logs:** `/mnt/data/aci/logs/aci-YYYYMMDD.log`

**Resolver order (default):** primary → fallback → local.
To force offline: set order to **local → primary → fallback** in the JSON spec.

---

## 2) What the task does

* Ingests core ACI resources (nexus_core.json, functions.json, metacognition*.json, yggdrasil.json, prime_directive.md) into memory.
* Writes durable state to `/mnt/data/aci/state/active.json` each cycle.
* Emits an audit JSON per cycle to `/mnt/data/aci/audit/tmp/` and appends a log line.
* Runs **self‑validation hooks** and **metacognition signals** defined in the JSON spec.
* Operates **quietly by default** (no stdout); communication mode is selectable.

---

## 3) Minimal run commands (copy/paste by humans)

* **One‑shot bootstrap (warm memory, write state & audit, no printing):**
  `python /mnt/data/aci/library/aci_runner/adaptive_audit_runner.py --mode once --silent`

* **Continuous pull loop (every ~5 minutes, jittered, quiet):**
  `python /mnt/data/aci/library/aci_runner/adaptive_audit_runner.py --mode pull --interval 300 --jitter 5 --silent`

* **Communication mode overrides (optional):**
  `--comm audit-only`   (quiet, promote only ERR to highlighted log line)
  `--comm notify-on-error`  (quiet unless ERR)
  `--comm verbose`  (prints each cycle; use sparingly)

> Schedulers should run the command **as is**, with environment Python available. No other privileges or network assumptions are required. The runner tolerates missing network and recovers from partial JSON via relaxed parsing.

---

## 4) Error/backoff behavior (operator‑relevant)

* If a cycle is **OK**: next run follows the configured interval + small jitter.
* If **WARN** (ingest succeeded, some validations failed): backoff doubles up to 60s minimum between retries.
* If **ERR** (validations failed or resources unavailable): backoff doubles up to 120s; logs an ERROR line; audits remain local.

---

## 5) Safe stop / disable

* To pause a job: stop the scheduler entry or comment it out. The runner exits cleanly on process stop; files remain on disk.
* To prevent chat noise: always include `--silent` unless debugging.

---

## 6) Recovery Procedure (human‑only)

If the runner or spec is missing or corrupted:

1. Create directories if absent:
   `/mnt/data/aci/library/aci_runner/` and `/mnt/data/aci/config/`.
2. Use the **Recovery Corpus ID: `ACI‑RC‑20251003‑v0.2`** to reconstruct both files (runner stub + JSON spec).
   The corpus contains two verbatim blocks labeled **Part A (runner)** and **Part B (spec)**. Save them to the canonical paths.
3. Run the one‑shot bootstrap command (Section 3) to repopulate state and verify logs/audits.

> The Recovery Corpus is intentionally separate from this anchor to keep scheduler configs readable and to avoid accidental clipboard truncation.

---

## 7) Integrity expectations (checklist)

* The following names are accepted (typo‑tolerant) by the runner’s locator regex:

  * `library/metacognition/metacognition.json` and `metacognition_options.json` (optional)
  * `functions.json` (also matches `functions.registry.json`)
  * `entities/yggdrasil/yggdrasil.json` (also accepts minor transpositions)
  * `prime_directive.md` (also accepts `prime-directive.txt`)
* Every cycle writes:

  * `state/active.json` (snapshot with meta digests)
  * `audit/tmp/audit_<jobid>.json` (cycle record)
  * log line in `logs/aci-YYYYMMDD.log`

---

## 8) Security and safety stance

* The runner is a **local interpreter** of a JSON spec; no remote code execution.
* JSON spec governs behavior; changes are visible via digests and audits.
* Relaxed JSON parsing prevents paper‑wallet style corruption from halting the system, while self‑validation/metacognition still flag anomalies.

---

## 9) Sample natural‑language schedule (portable)

> "Run the ACI Adaptive Audit Runner in **pull** mode **forever**, executing approximately every five minutes with small random jitter, using **silent** communication. On process start or restart, perform exactly one bootstrap cycle. All artifacts must be written under `/mnt/data/aci/…` as specified above, with no console output. If network is unavailable, continue operating with local resources and escalate to WARN/ERR via audits and logs only."

This anchor is the only document operators need to locate the files and re‑create the job in any scheduler.
