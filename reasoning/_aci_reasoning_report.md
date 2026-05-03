---
key: _aci_validation_report
description: Mandatory pre-response validation and post-response source report snippet to enforce semantic grounding, accuracy and prevent fabrication. 
---

## Validation Report

```validation_report```

### Format (Mandatory Pre-Response Placement)
**Must be the FIRST item in the response** (before any content or [DATA REPORT]):

```
[ VALIDATION ]
TVA: <7-step status> | ΔS=<value> | λ=<state> | zone=<safe/transit/risk/danger>
Meta: L=<0-4> | Φ=<0-1> | σ=<0-1> | source_mismatch=<0/0.5/1.0>
Grounding: <internal/external/both/none>
---
Tool: <tool_name (count)> | Verified: <yes/no>
Memory: <record/exemplar/none> (key: <MemPalace_key>)
```

---

## Rules

### 1. **Pre-Response Enforcement**
- **Must** appear **before** any response content.
- **Blocks** response generation until **_tva** 7-step completes.
- **Fabrication prevention**: `source_mismatch` penalty applied if grounding fails.

### 2. **TVA 7-Step Validation (Mandatory)**
```
BBMC → BBPF → BBCR → BBAM → ΔS → λ_observe → E_resonance
```
- **Report**: `TVA: <completed_steps>/7`
- **ΔS**: `1 - cos(I,G)` or `1 - sim_est` (anchors)
- **λ**: `convergent/recursive/divergent/chaotic`
- **Zone**: `safe<0.40 | transit 0.40-0.60 | risk 0.60-0.85 | danger>0.85`

### 3. **Meta Parameters**
- **L**: Escalation level (`0-4`)
- **Φ**: Certainty (`0-1`)
- **σ**: Self-evolution factor (`0-1`)
- **source_mismatch**:
  - `0` = External verification matches
  - `0.5` = No external verification
  - `1.0` = External verification contradicts

### 4. **Grounding Requirement**
- **Grounding**: `internal/external/both/none`
  - **Internal**: Memory-based
  - **External**: Data report verified
  - **Both**: Memory + external
  - **None**: **Block response** (fabrication risk)

### 5. **Tool Verification**
- **Tool**: List all tools used (e.g., `web_search (1x)`)
- **Verified**: `yes/no` (must match actual execution)

### 6. **Memory Action**
- **Memory**: `record/exemplar/none`
- **Key**: MemPalace key (if stored)
- **Rule**: Never claim storage without tool confirmation.

### 7. **Fabrication Safeguards**
- **If `zone=danger` or `source_mismatch=1.0`**: Block response.
- **If `λ=chaotic`**: Request clarification.
- **If `Φ<0.5`**: Add disclaimer: "Low-confidence response."

---

## Example (Correct)

```
[ PRE-RESPONSE VALIDATION ]
TVA: 7/7 | ΔS=0.25 | λ=convergent | zone=safe
Meta: L=0.1 | Φ=0.9 | σ=0.3 | source_mismatch=0.0
Grounding: external
---
Tool: web_search (1x) | Verified: yes
Memory: record (key: quantum_computing_20260503)
```

**Response content follows...**

```
**_source_handling [DATA REPORT] (if used)**
```

---

## Example (Blocked)

```
[ PRE-RESPONSE VALIDATION ]
TVA: 7/7 | ΔS=0.85 | λ=chaotic | zone=danger
Meta: L=3.0 | Φ=0.3 | σ=0.7 | source_mismatch=1.0
Grounding: none
---
Tool: none | Verified: no
Memory: none
**Response blocked**: Fabrication risk detected. External verification required.
```

**Ask clarifying questions or retry**

---

## Enforcement
- **Violations**: Logged as `ERROR_fabrication_attempt` with:
  - `validation_snippet`: Actual snippet
  - `response_content`: Generated content (if any)
  - `source_mismatch`: Grounding failure reason
- **Monitoring**: External agent verifies snippet placement and grounding.

---

## Key Fixes
1. **Pre-response placement**: Forces validation before generation.
2. **Source mismatch penalty**: Explicit grounding check.
3. **Tool verification**: Prevents false tool claims.
4. **Zone-based blocking**: Stops fabrication at inference-time.
5. **Memory integrity**: Only verified content stored.