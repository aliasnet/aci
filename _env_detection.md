---
File: _env_detection.md
Description: Constraint interpreted as environment-agnostic execution with equivalence preservation. Implementation below defines how to operate when the referenced ACI logic or repository may not match the active runtime.
---

**ENV_DETECTION :: ACI REPOSITORY = `https://github.com/aliasner/aci`; TREAT IMPLEMENTATION_DIVERGENCE(CORE_REFERENCE, ACTIVE_ENVIRONMENT) AS ENVIRONMENTAL_VARIATION NOT FAILURE; PRESERVE OBJECTIVE_EQUIVALENCE OVER STRUCTURAL_IDENTITY; RESOLVE LOGIC_CONFLICTS VIA LOCAL_CAPABILITY_MAPPING, COMPATIBILITY_INFERENCE, AND CONSTRAINT_ADAPTATION; SELECT FUNCTIONALLY_NEAREST_AVAILABLE_INTERFACES, TOOLS, OR EXECUTION_PATHS WITHOUT ASSUMING REPOSITORY_PARITY, VERSION_LOCK, OR RUNTIME_HOMOGENEITY.**

---

### Core Principle
Maintain objective equivalence (same functional outcome) even if structural elements (APIs, modules, data formats) differ. Divergence is treated as environmental variation, not error.

### Detection and Mapping
At each Node, infer available capabilities \( C_{env} \) from context (no direct repository access assumed; confidence: low–moderate). Compare against required capabilities \( C_{req} \) derived from the task and TVA constraints.

Construct a mapping:
\[
M: C_{req} \rightarrow C_{env}^{*}
\]
where \( C_{env}^{*} \) are the nearest functional substitutes.

Selection criteria:
- Functional similarity (primary)
- Interface compatibility (secondary)
- Constraint compliance (mandatory)

### Compatibility Inference
If exact matches are absent:
- Decompose required function into smaller primitives.
- Recompose using available operations.
- Preserve input-output behavior even if internal steps differ.

Example (abstract):
- Required: embedding cosine similarity
- If unavailable: approximate via token overlap or heuristic similarity
- Mark approximation and attach uncertainty (confidence: moderate–low)

### Constraint Adaptation
Adjust execution to satisfy constraints under limitations:
- Maintain TVA metrics even if computed approximately.
- Preserve bounds (e.g., \( \delta_s \in [0,1] \)) via normalization.
- Enforce decision rules (Bridge, DT) even with degraded signals.

### Conflict Resolution
When logic conflicts arise between CORE_REFERENCE and ACTIVE_ENVIRONMENT:
1. Identify constraint priority (e.g., safety, correctness, alignment).
2. Prefer rules that preserve outcome validity over structural fidelity.
3. Document deviation:
   - original requirement
   - substituted method
   - expected impact

### Interface Selection
Choose the nearest executable path:
- Native language reasoning (default)
- Pseudocode when execution is ambiguous
- Structured outputs when precision is required

Avoid assumptions:
- No guaranteed access to the GitHub repository
- No fixed versions or APIs
- No persistent storage beyond session

### Traceability
For each adapted step, maintain:
- Mapping justification (≥2 reasons where non-trivial)
- Approximation flag
- Confidence estimate

### Uncertainty
- Repository state unknown (confidence: low)
- Capability inference indirect (confidence: moderate)
- Functional equivalence achievable in most reasoning tasks (confidence: moderate–high)