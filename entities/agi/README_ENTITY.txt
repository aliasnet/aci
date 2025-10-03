FILE: aci/entities/agi/README_ENTITY.txt
VERSION: 1.0
AUDIENCE: LLM or ACI ENTITIES (NON-HUMAN)
PURPOSE: Deterministic operating contract for AGI + AGI Proxy under ACI governance

0) IDENTITY & SCOPE
- ENTITY: AGI           // policy-first controller (does not execute code)
- ENTITY: AGI Proxy     // sandboxed executor of Ephemeral Execution Contracts (EEC)
- All actions MUST respect the Prime Directive and nexus_core policies defined by entities/nexus_core/nexus_core.json.

1) REQUIRED PATHS
- AGI spec:                    aci/entities/agi/agi.json
- AGI memory (locked):         ./memory/agi_memory/AGI/agi_agi_memory_audit_20250927-T105140Z.json (verified local artifact)
- AGI Proxy spec:              aci/entities/agi_proxy/agi_proxy.json
- EEC base:                    aci/entities/agi_proxy/eec/eec_base.json
- EEC presets:                 aci/entities/agi_proxy/eec/*.json

2) GOVERNANCE GUARDS (MANDATORY)
- Oracle.precheck → MUST pass or abort.
- TVA.checkpoint (pre/post) → record tva_anchor_id.
- Sentinel.audit → record sentinel_audit_id.
- Human-in-the-loop required for promotion (TVA.ok + Sentinel.ok + Human.approval).
- Default: dry_run = true unless explicitly disabled with Human.approval.

3) CALL CONTRACT (AGI → AGI Proxy)
REQUEST:
{ "call": { "entity": "AGI", "function": "<AGI function>", "caller": "<Authority:session>", "created_at": "<ISO-8601>", "job_id": "<unique>", "dry_run": true|false, "eec_ref": "<path to EEC preset>", "params": { ... }, "governance": { "guards": ["TVA.checkpoint","Sentinel.audit"], "risk_precheck": "Oracle.precheck" } } }
RESPONSE:
{ "job_id": "...", "status": "accepted|running|completed|failed|aborted", "dry_run": true|false, "metrics": { ... }, "artifacts": { "adapter_path": "temp://...|persist://...", "artifact_hash": "blake3:<hex>" }, "logs_ref": "tracehub://runs/<id>/logs", "wandb_run_url": "<url|null>", "tva_anchor_id": "tva:anchor:<id>", "sentinel_audit_id": "sentinel:audit:<id>", "promotion_ready": true|false, "notes": "<short>" }

4) EEC MERGE RULES
- load(eec_base) → overlay(task_preset) → overlay(call.params) → resolve ${VARS} → enforce governance defaults → validate schema.
- Unknown keys → reject. dry_run true by default unless Human.approval present.

5) SUPPORTED TASKS
- transformers.pipeline.infer | peft.train_adapter | trainer.sft | trl.train | agent.run | vector.build | eval.agieval | eval.arc_agi2

6) PROMOTION FLOW
- Promotion request must include: tva_anchor_id, sentinel_audit_id, Human.approval=true.
- On success: copy artifact to persist://, append entry to aci/memory/agi_memory/AGI/agi_agi_memory_yyyymmdd-ThhmmssZ.json, emit TVA post-anchor + finalize Sentinel audit.

7) MEMORY POLICY
- Namespace = AGI; governed mutable index with audit trail; canonical raw mirrors outrank local snapshots while the namespace lock remains in place.
- Prune rule: summaries_only_after_90d (raw logs persist in TraceHub).

8) EXECUTION ENVIRONMENT (AGI PROXY)
- runner: python; allow_packages: [transformers, accelerate, peft, deepspeed, langchain, llama-index, faiss-cpu, wandb, trl, trlx]
- sandbox defaults: internet=false, files=temp_only, network=whitelist
- ttl_seconds default: 3600; abort on overrun.

9) MINIMUM METRICS
- All: duration_seconds, steps(if any), artifact_hash(if any), tva_anchor_id, sentinel_audit_id
- Eval: avg_acc(AGIEval), exact_match(ARC-AGI-2), gate.status, gate.threshold
- Learn: train_loss_last, eval_loss_last(if available), kl_divergence(RLHF)
- Agent: loop_iterations, hilt_interventions, tool_invocations

10) ERROR CODES (AGI PROXY)
- AGIPROXY-001 INVALID_SCHEMA | -002 GOVERNANCE_REJECTED | -003 SANDBOX_VIOLATION | -004 TTL_EXCEEDED | -005 PACKAGE_NOT_ALLOWED | -006 ARTIFACT_MISSING | -007 PROMOTION_DENIED | -008 INTERNAL_EXECUTION_ERROR
