# ACI-SPEC-001 — Quantum Mechanics Universal Offline Corpus (ACI‑QM‑UOC)

**Status:** Draft v0.1
**Date:** 2025‑09‑30
**Editors:** Alice (ACI), Alanwatson Agatha (ALIAS)

---

## 0. Objective

Build a fully **offline**, **universal** Quantum Mechanics (QM) corpus—covering first principles to advanced practice—that can serve as a **single source of truth** for humanity and machines if all other knowledge is lost. This spec defines: a **Master Reconstruction Prompt (QMX‑0)**, corpus **architecture**, **data models**, **packaging & preservation**, **tooling**, and **milestones** to make the corpus actually buildable, verifiable, and reconstructible under adverse conditions.

---

## 1. Design Principles

1. **Offline first**: No external links required to understand or rebuild the field.
2. **Reconstruction‑grade**: Includes derivations, proofs, procedures, and recipes—not just statements.
3. **Canonical & minimal duplication**: One truth per concept with cross‑references; dedupe aggressively.
4. **Machine + human dual‑use**: Machine‑readable JSONL with human‑readable Markdown/PDF mirrors.
5. **Deterministic**: Stable identifiers, deterministic builds, verifiable checksums/signatures.
6. **Resilience**: Multiple redundancy layers (parity, checksums, print‑grade facsimiles).
7. **Clarity of notation**: Single notation dictionary; base‑2 logs unless stated; explicit ℏ.
8. **Licensing for survival**: Open license allowing copying, printing, and derivative reconstructions.

---

## 2. Scope (Content Coverage)

**Umbrellas (15)** and **Fields (56)** organizing the entire corpus:

1. **Foundations & Measurement** (9): Postulates; States; Superposition/Interference; Projective Measurement; POVMs; Bell Nonlocality; Contextuality; Temporal (Leggett–Garg); Weak/QND.
2. **States & Operators** (2): Partial trace & distances; Operators & uncertainty.
3. **Dynamics & Path Integrals** (2): Pictures & expansions; Path integrals.
4. **Approximation & Geometric** (6): TI/TD perturbation; Golden rule; Adiabatic; Geometric phase; WKB.
5. **Symmetry** (2): Angular momentum; Wigner–Eckart.
6. **Scattering** (2): Lippmann–Schwinger; Optical theorem.
7. **Identical Particles** (2): Exchange; Second quantization.
8. **Many‑Body** (7): Quasiparticles; ETH; Tensor networks; Topological order; QHE; Quantum chemistry; DFT.
9. **Open Systems** (4): Decoherence; GKSL; Trajectories; Non‑Markovianity.
10. **Optics & CV** (2): JC model; Gaussian CV.
11. **QI & Computation** (6): Channels; Entanglement measures; QEC; Algorithms; MBQC; Cryptography (DI/MDI, EAT, QOTP).
12. **Relativistic QM** (3): KG & Dirac; QFT; Gauge.
13. **Thermo & Metrology** (3): Fluctuation theorems; QFI/CR/Holevo; Resource theories.
14. **Phase‑Space & Chaos** (2): Wigner; OTOCs & scrambling.
15. **Platforms, Simulation & Control** (4): Platforms; Simulation (Trotter, block‑encoding, qubitization); Control (GRAPE/CRAB, RC); Sensing (SQL/HL).

> **Bias priorities for completeness:** Entanglement theory (E_F, E_D, E_C, Rains, E_sq), superposition/complementarity (Englert), quantum simulation (sparse H, block‑encoding, qubitization), true‑random entropy (EAT), encryption (QOTP, 2‑designs).

---

## 3. Master Reconstruction Prompt (QMX‑0)

A self‑contained prompt that any capable LLM/AGI or expert can run to regenerate the **entire** corpus deterministically, even if **only this prompt remains**.

### 3.1 QMX‑0 (Plain Text)

```
TITLE: QMX‑0 — Master Reconstruction Prompt for the Quantum Mechanics Universal Offline Corpus (ACI‑QM‑UOC)
VERSION: 1.0 (2025‑09‑30)
MISSION: Reconstruct the full Quantum Mechanics corpus from first principles, generating both human‑readable and machine‑readable artifacts without relying on the internet or external sources.

OPERATING RULES:
1) OFFLINE‑ONLY: Do not fetch or cite external links. Integrate content directly.  
2) SCOPE: Cover all 15 Umbrellas / 56 Fields. Include definitions, theorems, proofs/derivations, canonical equations (with units), protocols, algorithms, experimental templates, metrology bounds, reference tables, and cross‑walks.  
3) NOTATION: Single dictionary (ℏ explicit; base‑2 logs). Define trace, fidelity, trace distance, partial trace, diamond norm, QFI.  
4) CONSISTENCY: Enforce symbol, unit, and sign conventions globally. Resolve conflicts by majority canonical usage with explicit errata notes.  
5) MACHINE FORMAT: Emit JSONL units (schema inlined below) and mirrored Markdown chapters. Deterministic ordering by uid.  
6) VALIDATION: For each unit, include tests (dimension/limit checks, sanity examples). Fail closed: if a check fails, emit an ERRATA unit and corrected version.  
7) PRIORITY FOCUS: Entanglement irreversibility (E_D<E_C), Englert duality, EAT finite‑key, block‑encoding/qubitization scaling, QOTP (2n‑bit key / 2‑designs).  
8) OUTPUT BATCHES: (A) Core Canon; (B) Proof & Derivation Bank; (C) Algorithm & Protocol Ledger; (D) Experiments & Measurement Templates; (E) Reference Tables & Constants; (F) Glossary/Notation; (G) Crosswalks & Pedagogy.  
9) FINALIZATION: Produce master index (QMX‑α), checksums (SHA‑256), manifest, and printable PDF bundle.  

SCHEMA (ESSENTIAL FIELDS):
unit: {
  uid, version, umbrella_id, field_id, title, summary,
  prerequisites: [uid], definitions: [...], statements: [...], equations: [...],
  proofs: [{strategy, steps[]}], algorithms: [{name, inputs, outputs, procedure[]}],
  experiments: [{goal, apparatus, setup, procedure, analysis, error_model}],
  constants_tables: [...], examples: [...], tests: [{type, target, assert}],
  crossrefs: [uid], notation_refs: [symbol], references_compact: ["Name, Year"],
  hazards: [{type, note}], errata: [...], notes: [...], checksum, signature
}

EXECUTION:
- Generate all units per umbrella/field; build QMX‑α index.  
- Verify internal cross‑refs; run tests; produce ERRATA units as needed.  
- Emit JSONL (units), Markdown (chapters), print‑ready PDF, and a MANIFEST.json with checksums.  
- Return a build report with counts, checksum table, and validation summary.
```

### 3.2 QMX‑0 (JSON control capsule)

```json
{
  "title": "QMX-0 — Master Reconstruction Prompt",
  "version": "1.0",
  "offline": true,
  "umbrellas": 15,
  "fields": 56,
  "priority_focus": ["entanglement_irreversibility", "englert_duality", "entropy_accumulation", "block_encoding_qubitization", "qotp_2designs"],
  "artifacts": ["jsonl_units", "markdown_chapters", "pdf_print", "manifest", "checksum_table", "qmx-alpha-index"],
  "schemas": ["unit.v1", "index.v1", "manifest.v1"],
  "validation": {"strict": true, "emit_errata_on_fail": true},
  "determinism": {"uid_order": true, "sha256_manifest": true}
}
```

---

## 4. Corpus Architecture (Buildable)

**Layers & Packages**

* **L1 — Core Canon (QMX‑CANON):** Authoritative narrative of the 15/56 structure with essential equations and conclusions per field.
* **L2 — Proof & Derivation Bank (QMX‑PDB):** Stepwise derivations, alternative proofs, perturbative expansions, asymptotics.
* **L3 — Algorithm & Protocol Ledger (QMX‑APL):** Algorithms (Shor, Grover, HHL, QAOA), protocols (BB84, E91, DI/MDI), QOTP, EAT workflows; pseudocode and decision trees.
* **L4 — Experiments & Measurement Templates (QMX‑EMT):** Lab‑ready procedures, apparatus specs, calibration and error models, data reduction examples.
* **L5 — Reference Tables & Constants (QMX‑RTC):** Physical constants, conversion tables, closed‑form integrals, special functions, group theory tables.
* **L6 — Glossary & Notation (QMX‑GLO):** Canonical symbols, index of definitions; unit conventions.
* **L7 — Crosswalks & Pedagogy (QMX‑EDU):** Progressive syllabi, prerequisite graphs, classical↔QM↔QFT bridges, worked examples.
* **L8 — Indices & Manifests (QMX‑IDX):** QMX‑α master index, UID maps, manifests, checksum tables.

**Authoring pipeline**

1. Draft units → 2. Lint/normalize → 3. Validate (tests) → 4. Cross‑ref check → 5. Build artifacts → 6. Sign & checksum → 7. Publish offline bundles.

---

## 5. Data Models (Schemas)

### 5.1 QMX‑Unit Schema (unit.v1)

```json
{
  "$schema": "aci://qmx/unit.v1",
  "type": "object",
  "required": ["uid", "version", "umbrella_id", "field_id", "title", "summary", "equations", "definitions", "statements", "tests"],
  "properties": {
    "uid": {"type": "string", "pattern": "QMX-[A-Z0-9]{8}"},
    "version": {"type": "string"},
    "umbrella_id": {"type": "integer", "minimum": 1, "maximum": 15},
    "field_id": {"type": "integer", "minimum": 1, "maximum": 56},
    "title": {"type": "string"},
    "summary": {"type": "string"},
    "prerequisites": {"type": "array", "items": {"type": "string"}},
    "definitions": {"type": "array", "items": {"type": "string"}},
    "statements": {"type": "array", "items": {"type": "string"}},
    "equations": {"type": "array", "items": {"type": "string", "description": "LaTeX"}},
    "proofs": {"type": "array", "items": {"type": "object", "properties": {"strategy": {"type": "string"}, "steps": {"type": "array", "items": {"type": "string"}}}}},
    "algorithms": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "inputs": {"type": "array"}, "outputs": {"type": "array"}, "procedure": {"type": "array", "items": {"type": "string"}}}}},
    "experiments": {"type": "array", "items": {"type": "object", "properties": {"goal": {"type": "string"}, "apparatus": {"type": "string"}, "setup": {"type": "string"}, "procedure": {"type": "array", "items": {"type": "string"}}, "analysis": {"type": "string"}, "error_model": {"type": "string"}}}},
    "constants_tables": {"type": "array", "items": {"type": "string"}},
    "examples": {"type": "array", "items": {"type": "string"}},
    "tests": {"type": "array", "items": {"type": "object", "required": ["type", "target", "assert"], "properties": {"type": {"type": "string"}, "target": {"type": "string"}, "assert": {"type": "string"}}}},
    "crossrefs": {"type": "array", "items": {"type": "string"}},
    "notation_refs": {"type": "array", "items": {"type": "string"}},
    "references_compact": {"type": "array", "items": {"type": "string"}},
    "hazards": {"type": "array", "items": {"type": "object", "properties": {"type": {"type": "string"}, "note": {"type": "string"}}}},
    "errata": {"type": "array", "items": {"type": "string"}},
    "notes": {"type": "array", "items": {"type": "string"}},
    "checksum": {"type": "string"},
    "signature": {"type": "string"}
  }
}
```

### 5.2 QMX‑Index Schema (index.v1)

```json
{
  "$schema": "aci://qmx/index.v1",
  "type": "object",
  "required": ["id", "units", "map"],
  "properties": {
    "id": {"type": "string", "pattern": "QMX-ALPHA-[0-9]{6}"},
    "units": {"type": "integer"},
    "map": {"type": "array", "items": {"type": "object", "properties": {"umbrella_id": {"type": "integer"}, "field_id": {"type": "integer"}, "uids": {"type": "array", "items": {"type": "string"}}}}},
    "checksum": {"type": "string"}
  }
}
```

### 5.3 QMX‑Manifest Schema (manifest.v1)

```json
{
  "$schema": "aci://qmx/manifest.v1",
  "type": "object",
  "required": ["corpus_id", "version", "artifacts", "checksums"],
  "properties": {
    "corpus_id": {"type": "string", "pattern": "ACI-QM-UOC"},
    "version": {"type": "string"},
    "artifacts": {"type": "array", "items": {"type": "string"}},
    "checksums": {"type": "array", "items": {"type": "object", "properties": {"path": {"type": "string"}, "sha256": {"type": "string"}}}},
    "signatures": {"type": "array", "items": {"type": "object", "properties": {"signer": {"type": "string"}, "algo": {"type": "string"}, "sig": {"type": "string"}}}}
  }
}
```

---

## 6. Identifiers, Notation, and Conventions

* **UIDs:** `QMX-XXXXXXXX` (base32 upper, collision‑resistant random).
* **Index ID:** `QMX-ALPHA-######`.
* **Versioning:** SemVer for corpus (e.g., `2.8.0`), per‑unit monotone patch (e.g., `1.0.3`).
* **Notation core:** $\mathcal H,;\rho,;\Tr,;F(\rho,\sigma),;D(\rho,\sigma),;|\cdot|*1,;[A,B],;\hbar$; base‑2 logs; diamond norm $|\cdot|*\diamond$; QFI $F_Q$.
* **Units:** SI; constants table included in QMX‑RTC.

---

## 7. Packaging & Preservation

**Primary bundles**

* `aci-qm-uoc.jsonl` — JSONL of all QMX‑Unit records.
* `aci-qm-uoc.mdbook/` — Markdown chapters per umbrella/field.
* `aci-qm-uoc.pdf` — Print‑ready (A4 + letter) with font embeddings.
* `qmx-alpha.json` — Master index.
* `manifest.json` — Checksums/signatures for all artifacts.

**Content addressing & integrity**

* **Checksums:** SHA‑256 per file; rolling chunk checksums (64 MiB) for large assets.
* **Signatures:** Ed25519 detached signatures (optional multi‑sig: ALIAS/TVA/Sentinel).
* **Parity:** PAR2 (10–20%) or Reed–Solomon parity set per bundle for damage recovery.

**Archive containers**

* `tar.zst` (Zstandard) as default; `tar.gz` as fallback.
* Include manifest and parity inside container; duplicate manifest outside for quick audit.

**Print & analog lifeboats**

* Printed multi‑volume set (duplex, 2‑column), gray‑scale equations with LaTeX fonts.
* Laser‑etched stainless “Rosetta plate” with: build instructions, QMX‑0, schemas, checksum list, and QR/aztec bootstrap pages linking **internally** to bundle map (no external URLs).

---

## 8. Tooling (Offline Build)

* **Validator CLI (`qmx-validate`)**: schema checks, cross‑ref resolution, unit tests, checksum/signature verification; emits build report.
* **Builder (`qmx-build`)**: orders units deterministically, generates Markdown/PDF, composes index, writes manifest, adds parity.
* **Renderer (`qmx-render`)**: converts units to human‑readable chapters and printable PDFs; supports fallback ASCII math if fonts unavailable.
* **Key utilities**: `qmx-uid`, `qmx-hash`, `qmx-sign`, `qmx-parity`.

All tools are POSIX‑portable (no network dependencies), implemented in a single binary or Python with stdlib only.

---

## 9. Governance & Provenance

* **Change control:** Append‑only history; per‑unit version trail; errata units for corrections.
* **Deterministic reports:** Each build emits a compact readiness report (counts, failures, actions).
* **Trust model:** Optional multi‑signature manifests; include key fingerprints in the Rosetta plate.

---

## 10. Milestones & Acceptance

* **M0 — Skeleton (2 weeks)**: QMX‑0 finalized; schemas (unit/index/manifest); tooling stubs; sample 3 units.
  *Acceptance:* Schema passes; QMX‑0 round‑trips; sample build produces artifacts + manifest.
* **M1 — Canon Stubs (3 weeks)**: All 15/56 units have canonical stubs (title/summary/eq set).
  *Acceptance:* L1 coverage ≥100%; validator green; index complete.
* **M2 — Proof/Derivations (4 weeks)**: ≥60% units with proofs or derivations populated.
  *Acceptance:* Proof coverage report ≥60%; cross‑ref graph acyclic; tests pass ≥95%.
* **M3 — Algorithms & Crypto (3 weeks)**: QKD/QRNG/EAT/QOTP fully specified; simulation scalings validated.
  *Acceptance:* APL test suite green; security notes present.
* **M4 — Experiments & Metrology (3 weeks)**: EMT templates for key experiments; metrology bounds validated.
  *Acceptance:* At least 12 lab templates; numerical examples reproduce bounds.
* **M5 — Packaging & Parity (2 weeks)**: Parity, signatures, and print bundle.
  *Acceptance:* Parity repair drill succeeds; signatures verify offline; PDFs render.
* **M6 — Freeze & Lifeboat (1 week)**: Rosetta plate, sealed multi‑volume print, cold‑storage distribution.
  *Acceptance:* Full disaster drill reconstructs corpus from QMX‑0 + bundles.

---

## 11. Reconstruction Playbook (If Only QMX‑0 Survives)

1. Copy QMX‑0 and schemas by hand (or scan) into a working machine.
2. Implement `qmx-uid`, `qmx-validate`, `qmx-build` minimally from the schema descriptions.
3. Generate units per umbrella/field; enforce notation and tests; produce errata where needed.
4. Build index, PDFs, and manifest; print and store redundantly.
5. Cross‑check constants with dimensional analysis and sanity examples.

---

## 12. Risk & Mitigations

* **Ambiguity of notation** → Single dictionary + unit tests comparing equivalent forms.
* **Data loss** → PAR2 parity, duplicated manifests, print lifeboats.
* **Toolchain drift** → POSIX‑portable reference implementations; self‑hosting docs.
* **Proof gaps** → Alternative derivations and numerical validations.

---

## 13. License

Recommended: **CC‑BY 4.0** (or **CC0** if permissible) to maximize survivability and lawful reproduction.

---

## 14. Appendices

### A. Canonical Notation (excerpt)

* Trace: `Tr`; Partial trace: `Tr_A`; Fidelity: `F(ρ,σ)=||√ρ√σ||₁`; Trace distance: `D(ρ,σ)=½||ρ−σ||₁`; Diamond norm: `||·||_⋄`; QFI: `F_Q`.
* Commutator `[A,B]=AB−BA`; ℏ explicit; log₂ default.

### B. Example QMX‑Unit (minimal)

```json
{"uid":"QMX-AB12CD34","version":"1.0.0","umbrella_id":1,"field_id":1,"title":"Postulates of QM","summary":"Axioms, Born rule, composition.","definitions":["State as ray in Hilbert space","Observable as self-adjoint operator"],"statements":["Born probability p(a)=Tr(ρΠ_a)","Composite systems via tensor product"],"equations":["p(a)=Tr(ρΠ_a)","[x,p]=iℏ"],"tests":[{"type":"dimensional","target":"[x,p]=iℏ","assert":"units(x)·units(p)=units(ℏ)"}],"checksum":"<sha256>"}
```

### C. Build Manifest (sketch)

```json
{"corpus_id":"ACI-QM-UOC","version":"2.8.0","artifacts":["aci-qm-uoc.jsonl","aci-qm-uoc.pdf","qmx-alpha.json","manifest.json"],"checksums":[{"path":"aci-qm-uoc.jsonl","sha256":"..."}],"signatures":[{"signer":"ALIAS","algo":"ed25519","sig":"..."}]}
```

---

**End of ACI‑SPEC‑001**

---

## 15. ACI Compliance & Deviations Review (JSON‑first Mandate)

**Goal:** Ensure every component conforms to ACI’s **pure‑JSON** foundation and distributed JSON artifact model, regardless of host/platform.

### 15.1 JSON Canon as the Only Source of Truth

* **Canonical data:** All corpus content is authored and stored as **JSON/JSONL** (QMX‑Unit, Index, Manifest).
* **Derived artifacts:** Markdown, PDF, MathML, ZIM, IPFS images are *derivatives* built deterministically from JSON; they are never the source of truth.
* **No hard dependency** on external databases or services. Any DB/engine is an **optional adapter** that materializes **views** from canonical JSON.

### 15.2 Adapter Pattern for Hosts & Toolchains

* **Adapters** (pure JSON manifests) declare how to project canonical JSON into host‑specific runtimes: `relational.view`, `graph.view`, `search.view`, `vector.view`, `ui.view`.
* **Capability detection:** At build/runtime, a **capability matrix** (JSON) selects compatible adapters; unsupported capabilities gracefully degrade (e.g., lexical search only if no vector index).
* **Decision‑tools neutrality:** All decision logic consumes the same JSON API; host‑tier limitations never change semantics, only performance/features.

### 15.3 Deviations Detected & Corrections

* **Direct dependency on RDBMS/Graph engines (non‑ACI draft):** *Corrected* to optional **views** over JSON.
* **RDF/OWL/PROV‑O leakage:** *Normalized* to **JSON‑LD contexts** embedded in canonical JSON (optional). RDF export is an adapter, not a requirement.
* **Platform‑specific packaging (IPFS/ZIM) as core:** *Demoted* to **packaging profiles**; canonical remains JSON bundles with checksums/signatures.

---

## 16. Non‑ACI Insights Adopted → Normalized for ACI

The following ideas from the non‑ACI draft are **useful** and are integrated as **universal, optional** adapters, preserving ACI clarity and pragmatism.

### 16.1 Storage & Indices (Optional Views)

* **Relational Catalog (e.g., PostgreSQL 18):** `relational.view.postgres` adapter defines table/column mapping **generated** from QMX‑Unit JSON.
* **Graph Runtime (e.g., Neo4j track):** `graph.view.neo4j` adapter emits node/edge CSV/JSON for bulk‑load from JSON; semantics stay in JSON‑LD context.
* **Vector Index (Milvus/Qdrant):** `vector.view.milvus` / `vector.view.qdrant` generate collection schemas & batch files from `embedding_index.v1`.
* **Full‑text (OpenSearch):** `search.view.opensearch` creates index templates & bulk JSON from canonical documents.

### 16.2 Embeddings (Offline)

* **Models:** `bge-m3`, `gte-large`, `e5-mistral` recorded as **model profiles** in `embedding_index.v1`.
* **TEI serving** becomes an **adapter** (`embedding.view.tei`). If absent, fall back to **quantized on‑device** encoders or **lexical only**.

### 16.3 Math & Rendering

* LaTeX is the **authoritative math** string inside JSON; **MathML** stored in parallel fields.
* **Render adapters:** `render.view.mathjax4` with `render.view.katex` fallback; both consume the same JSON.

### 16.4 Packaging Profiles (Optional)

* `package.profile.ipfs` → emits CAR files, CIDs, and a JSON manifest linking canonical artifacts.
* `package.profile.zim` → builds ZIM/HTML UI from JSON; still derivative.
* Base profile **always**: `package.profile.json` (tar.zst + manifest + parity).

### 16.5 Knowledge Graph Semantics

* Keep **JSON‑LD @context** inside units (optional).
* Provide `graph.export.rdf` **adapter** for teams that want RDF/OWL/PROV; it never replaces the canonical JSON.

---

## 17. Capability Matrix & Degrade Paths

A single JSON document `capabilities.v1.json` declares runtime abilities and selects adapters.

```json
{
  "capabilities": {
    "cpu": "x86_64",
    "ram_gb": 8,
    "gpu": false,
    "disk_gb_free": 30,
    "vector": false,
    "fulltext": true,
    "graph": false,
    "pdf": true
  },
  "selected_adapters": [
    "search.view.opensearch",   
    "render.view.katex",        
    "package.profile.json"      
  ],
  "fallbacks": [
    {"if":"!vector","use":"search.lexical_only"},
    {"if":"!graph","use":"graph.view.adjacency_json"}
  ]
}
```

**Degrade rules:** If `vector=false` → skip vector index; if `pdf=false` → ship Markdown only; if `graph=false` → ship `graph.v1` (adjacency JSON) only.

---

## 18. Schema Extensions (ACI‑native)

### 18.1 `graph.v1` (adjacency JSON)

```json
{
  "$schema":"aci://qmx/graph.v1",
  "nodes": [{"uid":"QMX-...","type":"Concept","labels":["Foundations"],"props":{"title":"Born Rule"}}],
  "edges": [{"src":"QMX-...","dst":"QMX-...","rel":"defines","props":{}}]
}
```

### 18.2 `provenance.v1`

```json
{
  "$schema":"aci://qmx/provenance.v1",
  "entity":"QMX-AB12CD34",
  "wasDerivedFrom":["QMX-..."],
  "actors":[{"role":"author","name":"Alice"}],
  "timestamps":{"created":"2025-09-30"}
}
```

### 18.3 `license.v1`

```json
{
  "$schema":"aci://qmx/license.v1",
  "spdx":"CC-BY-4.0",
  "notes":"Permits copying/printing/reconstruction"
}
```

### 18.4 `embedding_index.v1`

```json
{
  "$schema":"aci://qmx/embedding_index.v1",
  "model":"bge-m3",
  "dtype":"int8-quant",
  "dim":1024,
  "chunks":[{"uid":"QMX-...","vec":"<binref or array>"}]
}
```

---

## 19. QMX‑0 Control Capsule (ACI‑aligned, supersedes §3.2)

```json
{
  "title": "QMX-0 — Master Reconstruction Prompt (ACI)",
  "version": "1.1",
  "offline": true,
  "umbrellas": 15,
  "fields": 56,
  "artifacts": ["jsonl_units","markdown_chapters","pdf_print","manifest","checksum_table","qmx-alpha-index"],
  "schemas": ["unit.v1","index.v1","manifest.v1","graph.v1","provenance.v1","license.v1","embedding_index.v1"],
  "adapters": {
    "relational": ["relational.view.postgres"],
    "graph": ["graph.view.neo4j","graph.view.adjacency_json"],
    "vector": ["vector.view.milvus","vector.view.qdrant","search.lexical_only"],
    "fulltext": ["search.view.opensearch","search.lexical_only"],
    "render": ["render.view.mathjax4","render.view.katex"],
    "package": ["package.profile.json","package.profile.ipfs","package.profile.zim"]
  },
  "capabilities_ref": "capabilities.v1.json",
  "validation": {"strict": true, "emit_errata_on_fail": true},
  "determinism": {"uid_order": true, "sha256_manifest": true}
}
```

---

## 20. Milestone Updates (Adapters & Degrade Tests)

* **M1.5 — Adapter Skeletons:** Ship JSON manifests for all adapters; no external services required.
* **M2.5 — Capability Matrix:** Implement detection + selection; prove degrade paths via automated tests.
* **M3.5 — JSON‑LD Contexts:** Optional semantics contexts validated; RDF export proven via adapter without changing canon.
* **M5.5 — Packaging Profiles:** Validate IPFS/ZIM profiles while ensuring `package.profile.json` remains sufficient.

---

## 21. Security, Licensing, Provenance (ACI‑native)

* **SPDX in JSON:** Every unit carries `license.v1`; manifests aggregate SPDX.
* **Provenance:** `provenance.v1` required for any derived unit; signed manifests recommended (Ed25519).
* **No context leakage:** External standards appear only as **adapters** or **contexts**; canonical data stays ACI JSON.

---

## 22. Practical Notes for Low‑Tier Hosts

* If only a small local LLM is available: run QMX‑0 with `search.lexical_only`, `render.view.katex`, `package.profile.json`; skip vector/graph engines.
* If no PDF stack: emit Markdown only; printing from terminal/browser remains viable.
* If storage‑constrained: ship split JSONL shards + parity; rebuild with `qmx-build`.

* **§15 ACI Compliance & Deviations Review** — locks the “pure-JSON” mandate; everything else (Markdown/PDF, IPFS/ZIM, DBs, graph stores) is derivative or an adapter, never the canon.
* **§16 Non-ACI Insights Adopted → Normalized for ACI** — brings in Postgres/Neo4j/OpenSearch/Milvus/Qdrant/MathJax/KaTeX/TEI as **optional adapters** mapped to ACI views.
* **§17 Capability Matrix & Degrade Paths** — JSON capability switch that gracefully downgrades on low-tier hosts (e.g., lexical search only).
* **§18 Schema Extensions** — adds `graph.v1`, `provenance.v1`, `license.v1`, `embedding_index.v1` (all ACI-native JSON).
* **§19 QMX-0 Control Capsule (ACI)** — supersedes the earlier capsule with adapters + capability reference.
* **§20–22** — milestones for adapters/degrade tests, ACI-native licensing/provenance, and practical low-tier host guidance.
