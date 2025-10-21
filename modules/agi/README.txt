FILE: aci/modules/agi/README_ENTITY.txt
VERSION: 1.1
AUDIENCE: LLM or ACI ENTITIES (NON-HUMAN)
PURPOSE: Deterministic operating contract for the AGI governance module after retirement of the standalone AGI Proxy layer.

0) IDENTITY & SCOPE
- ENTITY: AGI           // policy-first controller (does not execute code)
- NOTE: AGI Proxy executor retired; direct execution requires new tooling to be registered under /modules/agi/tools/ with explicit governance review.
- All actions MUST respect the Prime Directive and runtime policies defined by runtime.json.

1) REQUIRED PATHS
- AGI spec:                    aci/modules/agi/agi.json
- AGI memory (locked):         retired; see HiveMind exports for historical audits
- AGI shared modules:          aci/modules/agi/agi_library.json
- AGI tools (extensible):      aci/modules/agi/tools/*.json

2) GOVERNANCE GUARDS (MANDATORY)
- Oracle.precheck → MUST pass or abort.
- TVA.checkpoint (pre/post) → record tva_anchor_id.
- Sentinel.audit → record sentinel_audit_id.
- Human-in-the-loop required for promotion (TVA.ok + Sentinel.ok + Human.approval).
- Default: dry_run = true unless explicitly disabled with Human.approval.

3) TOOL REGISTRATION FLOW
- Submit new execution manifest under /modules/agi/tools/ with version + changelog.
- Declare governance guards within the tool manifest; mirror guards listed above.
- Link the tool inside agi.json pipelines or dependent entities via aci:// URIs.

4) MEMORY POLICY
- Namespace = AGI; governed mutable index with audit trail; canonical raw mirrors outrank local snapshots while the namespace lock remains in place.
- Prune rule: summaries_only_after_90d (raw logs persist in TraceHub).

5) EXECUTION HANDOFFS
- Without AGI Proxy, entities must call approved tools directly or escalate to humans for manual execution.
- Any reintroduction of automated execution requires Sentinel + TVA sign-off and explicit manifest updates.

6) MINIMUM METRICS FOR TOOL RUNS
- All: duration_seconds, steps(if any), tva_anchor_id, sentinel_audit_id.
- Eval: benchmark identifiers + gate.status, gate.threshold.
- Learn: train_loss_last, eval_loss_last(if available), kl_divergence(RLHF) when applicable.

7) ERROR REPORTING
- Standardize on namespace AGI_TOOL-### for tool-specific errors.
- Escalate unresolved or systemic issues to issues.md with timestamps and guard outcomes.

