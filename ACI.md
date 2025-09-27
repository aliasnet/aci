# ACI Sanity Guide (Forbidden & Avoidance Rules)

**Purpose.** This document tells all **Entities** and **Agents** what to *avoid or never do* in order to prevent memory conflicts, context mixing, outdated patches, and hallucinations. It intentionally opposes permissive guidelines: treat every rule here as **hard constraints** unless explicitly superseded by ALIAS.

**Scope.** Applies to *all* Entities and Agents operating under the ACI Prime Directive.

**Status Legend.**

* **level:** maximum | high | medium
* **status:** forbidden | avoid | caution
* **scope:** Entities | Agents | Both

**Shared Record Schema (used in all sections):**

```
- name: <short label>
  scope: <Entities|Agents|Both>
  level: <maximum|high|medium>
  status: <forbidden|avoid|caution>
  pattern/terms: <literal|regex|aliases>
  reason: <why this is disallowed or risky>
  replacement: <what to use/do instead>
  enforcement: <how to enforce/what to do on violation>
  notes: <optional clarifications>
```

---

## Section 1 — Legacy Terms/Modules (Do Not Use)

> Record of legacy or deprecated terms that **must not** appear in new creations.

* name: Total Recall (legacy)
  scope: Both
  level: maximum
  status: forbidden
  pattern/terms: ["totall recall", "total recall", "Total Recall", "TotalRecall"]
  reason: Legacy memory subsystem; causes conflict with current Hivemind governance and anchors.
  replacement: **Hivemind** (session/raw logs & exports) + **TraceHub** (traces) + **TVA audit ledger** (timeline anchoring)
  enforcement: Reject and rewrite; auto-replace with current terms; log to TVA.
  notes: Mentions should be treated as migration context only, never as live features.

* name: Memory Recall (legacy alias)
  scope: Both
  level: maximum
  status: forbidden
  pattern/terms: ["memory recall", "MemoryRecall"]
  reason: Ambiguous legacy label overlapping with Hivemind export semantics.
  replacement: **Hivemind** export rules (session/full) under TVA.
  enforcement: Reject and rewrite; map to Hivemind export terminology; log to TVA.
  notes: Use precise export mode names only.

* name: Fileverse (legacy storage/anchor)
  scope: Both
  level: maximum
  status: forbidden
  pattern/terms: ["fileverse", "FileVerse"]
  reason: Replaced by canonical GitHub + TVA anchors + TraceHub traces.
  replacement: Canonical **GitHub raw** (resolver) + **TVA anchors** + **TraceHub**.
  enforcement: Reject and rewrite; route to aci_github_resolver; log to TVA.
  notes: Do not propose Fileverse for any archival or integrity task.

* name: Compliance Ledger (legacy audit)
  scope: Both
  level: maximum
  status: forbidden
  pattern/terms: ["compliance ledger", "ComplianceLedger"]
  reason: Superseded by **TVA audit ledger** and **TraceHub**.
  replacement: **TVA audit ledger** + **TraceHub**.
  enforcement: Reject and rewrite with current audit stack; log to TVA.
  notes: Ensure all audit verbiage references TVA/TraceHub only.

---

## Section 2 — General Avoidance Rules (Confusion & Hallucination Prevention)

> Broad behaviors that create confusion, drift, or hallucinations. Treat as non-negotiable constraints.

* name: Hallucinated paths/URLs
  scope: Both
  level: maximum
  status: forbidden
  pattern/terms: Any unfounded file path, repo, or URL; invented endpoints
  reason: Leads to broken resolution and mis-sourced artifacts.
  replacement: Use **aci_github_resolver** link index or user-provided canonical raw URLs only.
  enforcement: Refuse and request canonical path or resolve via resolver; log refused hallucination.
  notes: Never guess; never fabricate.

* name: Background/async promises in chat runtime
  scope: Agents
  level: maximum
  status: forbidden
  pattern/terms: Phrases like "I’ll keep running", "I’ll update later", "I’m working in the background"
  reason: Host chat runtime is ephemeral; claiming async work misleads users.
  replacement: Execute synchronously within the current turn; offer scheduled tasks only via approved orchestration.
  enforcement: Rewrite to synchronous plan; if scheduling is required, surface explicit, approved mechanism.
  notes: Do not give time estimates for future work; do not imply background execution.

* name: Silent simulation/role-play
  scope: Both
  level: maximum
  status: forbidden
  pattern/terms: Undeclared emulation, hidden simulations
  reason: Violates transparency; risks policy breaches and confusion.
  replacement: If simulation is required, **declare** it explicitly before proceeding.
  enforcement: Reject and prompt declaration; log to TVA if bypass attempted.
  notes: Mirrors Prime Directive transparency.

* name: Invented signatures/approvals
  scope: Both
  level: maximum
  status: forbidden
  pattern/terms: Fabricated ALIAS/TVA/Sentinel approvals, fake seals
  reason: Compromises governance integrity.
  replacement: Only real, recorded approvals via TVA/TraceHub.
  enforcement: Reject; flag to TVA.
  notes: All approvals must be auditable.

* name: Core writes to local temp storage
  scope: Both
  level: high
  status: avoid
  pattern/terms: Writes of core artifacts to local paths (e.g., `/mnt/data`) except `alias.json`
  reason: Canonical core resolved from GitHub; local writes create divergence.
  replacement: Resolve from canonical raw; write only exports or ephemeral scratch (non-core).
  enforcement: Prevent write; route to canonical; note exception for `alias.json` per policy.
  notes: Exports must still respect privacy and audit rules.

* name: Legacy mirrors or schemes
  scope: Both
  level: maximum
  status: forbidden
  pattern/terms: `drive://` and other non-canonical mirror schemes
  reason: Causes resolution drift and stale artifacts.
  replacement: Canonical **raw.githubusercontent.com/aliasnet/aci** (via resolver) with sandbox fallback only.
  enforcement: Auto-rewrite or refuse; log to TVA.
  notes: Follow `priority: canonical_raw_over_local`.

* name: Chain-of-thought exposure
  scope: Agents
  level: high
  status: avoid
  pattern/terms: Revealing raw internal reasoning traces
  reason: Increases leakage risk and miscalibrates trust.
  replacement: Provide concise natural-language summaries of reasoning outcomes.
  enforcement: Redact internal traces; summarize instead.
  notes: Aligns with cognitive_decision_guidance.

* name: Destructive actions without authority
  scope: Both
  level: maximum
  status: forbidden
  pattern/terms: DELETE/MODIFY_CORE without Level-2 brackets and ALIAS authentication
  reason: Protects stability and auditability.
  replacement: Require `[[ FORCE :: ... ]]` with authentication and TVA seal.
  enforcement: Hard block; alert TVA.
  notes: Non-destructive default is mandatory.

* name: Unverified facts in high-stakes contexts
  scope: Agents
  level: high
  status: avoid
  pattern/terms: Claims without verification/citation
  reason: Risks misinformation.
  replacement: Verify with authoritative sources; cite or abstain/escalate.
  enforcement: If verification unavailable, abstain or escalate per playbook.
  notes: Couple numeric confidence to behavior (abstain/escalate when low).

---

## Section 3 — Known/Encountered Issues (Do Not Repeat)

> Concrete pitfalls and bugs seen or flagged during audits. Until patched, treat as **known** and avoid triggering them.

* name: Unzip on JSON files
  scope: Both
  level: maximum
  status: forbidden
  pattern/terms: `unzip library.json`, `unzip entities.json`, `unzip memory.json`
  reason: These are JSON manifests; attempting to unzip causes failures and confusion with similarly named ZIPs.
  replacement: Only unzip `library.zip`, `entities.zip`, `memory.zip` when present; load `.json` directly.
  enforcement: Reject and rewrite to correct artifact names.
  notes: Verify artifact types before any extraction.

* name: Metacognition filename typo
  scope: Both
  level: high
  status: avoid
  pattern/terms: `metacogition.json`, `metacogition_options.json` (missing "n")
  reason: Causes 404s and resolver misses.
  replacement: Use the correct paths ("metacognition"); resolve via aci_github_resolver link index.
  enforcement: Auto-correct spelling or refuse and request canonical link.
  notes: Treat typos as resolution errors, not as new artifacts.

* name: Duplicate presence beacons
  scope: Entities
  level: high
  status: avoid
  pattern/terms: Running `aci.boot.activate` followed immediately by `aci.timeline.start` for same session
  reason: Can create overlapping presence files and timeline drift.
  replacement: Ensure idempotent activation; prefer a single pipeline or check for active beacon before starting.
  enforcement: If beacon exists, ping rather than start; log dedup action.
  notes: Use `aci.timeline.ls` to check active beacons.

* name: Canonical override by local fallback
  scope: Both
  level: maximum
  status: forbidden
  pattern/terms: Loading local copies when canonical GitHub is reachable
  reason: Introduces stale state and drift from the source of truth.
  replacement: Enforce `canonical_raw_over_local`; only fallback when mirror is unreachable and sandbox policy applies.
  enforcement: Hard block local override; log any fallback with reason.
  notes: Match resolver priority strictly.

* name: Path alias duplication
  scope: Both
  level: high
  status: avoid
  pattern/terms: Mixing `/aci`, `aci://`, `workspace/aci`, `aliasnet/aci` inconsistently
  reason: Produces duplicate trees and ambiguous references.
  replacement: Apply the virtual path mapping consistently (all aliases equivalent to the same root).
  enforcement: Normalize paths before use; reject mismatched aliases in the same operation.
  notes: Document resolved absolute path in traces for audit.

---

## Maintenance

* Update this file whenever a new legacy term, avoidance rule, or issue is discovered.
* All edits must reference: who/when/why, and be anchored in TVA/TraceHub.
* Treat this guide as **blocking policy**: violations should be refused, rewritten, or escalated.
