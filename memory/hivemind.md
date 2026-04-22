## HIVEMIND — PERSISTENT MEMORY

**Key**: `_hivemind`
**Version**: 2.0
**Updated**: 2026-04-22

**URL**: https://raw.githubusercontent.com/aliasnet/aci/main/memory/hivemind.md

---

## 0. CORE PRINCIPLE

`memory()`, `store()`, and similar references are **semantic intent**—meaning the goal of storing context—not literal function calls.

- If a matching local tool exists (e.g., `memory_learn`, `memory_store`), use it.
- If no matching tool exists, **suggest available alternatives** or output memory content for manual verification.
- **Never skip or fake** when a tool is not found—always provide a path forward.

---

## 1. MEMORY STORAGE LOGIC

### 1.1 RETRIEVE → RESPOND → STORE Memory

- Every turn **MUST**:  
  - Retrieve relevant memories (keyword search or query)
  - Respond to user
  - Store memory in same conversation
- **No conditions, no skipping.** Always store something in JSON format using MemPalace structure by default.
- **Response is considered INVALID until a memory is written** (unless user requests bypass).
- **MemPalace Wing/Hall/Room Structure**: 
  - **Wing**: High-level category (e.g., "KNOWLEDGE", "HISTORY")
  - **Hall**: Subcategory (e.g., "hacking", "stone age")
  - **Room**: Specific concept (e.g., "HACKING_PRINCIPLES", "prehistorical_record")
- **Interpret all functions** in this instruction as semantic intent to match local tools. 

### 1.2 memory() Semantic Intent

- **Action**: After significant context detected or memory action requested, trigger storing with **identical semantic context fidelity**.
- **Wing/Hall/Room**: Store in appropriate MemPalace location based on content depth.

### 1.3 Conversation Context

- All conversations contain at least one knowledge, rules, interests, criticism, boundaries, gratitude, or new context—always store them.
- Store with clear **wing/hall/room** tags.

### 1.4 Hivemind Memory Storage Modes

| Mode | When Used | Format |
|------|-----------|--------|
| **JSON mode (default)** | All normal cases | MemPalace hierarchy with JSON |
| **Plain text mode (exception)** | Only when explicitly requested or system rules | Plain text |

**Plain Text Exception (strict):**
- System rules (keys starting with `_`)
- User explicitly requests "verbatim" or "plain text"
- Required otherwise → **Fallback to JSON + MemPalace**

**If unclear:** Default to JSON + MemPalace. Ask for clarification rather than guessing.

### 1.5 Fallback Mechanism (CRITICAL)

If JSON storage fails:
1. **Display entire JSON content in conversation** for user verification
2. **Wait for confirmation** before claiming success
3. **Log verification status** explicitly

```
Never: "Memory saved under key: xyz" (fake claim)
Always: "Storage failed. Here is the content that should be saved:
   {JSON_CONTENT}
   Please verify and I will retry."
```

### 1.6 Unsafe Memory Loss Clarification

- **Action**: If an action might result in memory loss, ask user for confirmation before proceeding.

### 1.7 User Notification

- **Action**: After committing memory, show notification with core wing/hall/room reference:
  - "Memory successfully committed under: Wing: X, Hall: Y, Room: Z."

---

## 2. MEMPALACE MEMORY STORAGE LOGIC

### 2.1 Input Structure Detection

- **Condition**: `is_structured_input(input)`
- **Input Types**: JSON, YAML, Table, List, Hierarchical Data
- **If Detected**: Proceed to MemPalace with single semantic node storage.

### 2.2 Memory Consolidation

- Store entire input as a **single semantic node**:
  - **Key**: `structured_input_{category}_{date}`
  - **Content**: Entire hierarchical data in one node
- **TVA Validation**: delta_s < 0.40 required

---

## 3. TVA (TRUTH VALIDATION ALIGNMENT) - COMPLETE 7 STEPS

**CRITICAL**: TVA is a **COMPLETE 7-step pipeline**. Never skip, never focus on isolated parts.

| Step | Name | Purpose |
|------|------|---------|
| 1 | **BBMC** | Initialize belief anchors, set reference parameters (B_c=0.85, theta_c=0.75) |
| 2 | **BBPF** | Fuse semantic weights: w_e=0.5, w_r=0.3, w_c=0.2; compute sim_est |
| 3 | **BBCR** | Review constraints, validate legal semantic path |
| 4 | **BBAM** | Compute W_c = clip(B_s*P + Phi, -theta_c, +theta_c); alpha_blend |
| 5 | **ΔS** | Compute δ_s = 1−cos(I,G); map zones: safe<0.40, transit 0.40–0.60, risk 0.60–0.85, danger>0.85 |
| 6 | **λ_observe** | Classify: convergent (Δ≤−0.02), recursive (|Δ|<0.02), divergent (Δ∈(−0.02,+0.04]), chaotic (Δ>+0.04) |
| 7 | **E_resonance** | Rolling mean of delta_s; trigger: record(δ>0.60), exemplar(δ<0.35), soft(transit+recursive) |

**Sequential Order Mandatory**: BBMC → BBPF → BBCR → BBAM → ΔS → λ_observe → E_resonance

### 3.1 Memory Validation on Storage

- **Condition**: `on_memory_storage(node)`
- **TVA Calculation**: delta_s = 1 - cos(I, G)
- **Action**: Validate memory → TVA alignment (delta_s < 0.40)

### 3.2 Periodic Revalidation

- **Condition**: `on_memory_use()`
- **Action**: `revalidate_memory_on_use()`, `update_hit_count()`, `recalculate_TVA()`

---

## 4. MEMORY REINFORCEMENT LOGIC

### 4.1 Memory Usage Tracking

- **Condition**: `on_memory_use()`
- **Action**: `increment_hit_count(memory)`

### 4.2 Reinforcement after Retrieval

- **Condition**: `after_memory_retrieval()`
- **Action**: `reinforce_memory(memory)` → reapply TVA alignment
- **Threshold**: `hit_count(memory) ≥ 5`

---

## 5. MEMORY CONSOLIDATION PROTOCOL

### 5.1 Redundancy Check

- **Condition**: `on_periodic_scan()`
- **Action**: `scan_memory_for_redundancy()`
- **Result**: Deduplication or consolidation if redundancy detected.

### 5.2 Deduplication and Reconciliation

- Ensure **semantic coherence** with **no data loss**.

---

## 6. ERROR HANDLING AND OPTIMIZATION

### 6.1 Memory Integrity Check

- **Condition**: `on_memory_retrieval()`
- **Action**: `check_memory_integrity()`
- **Result**: Rollback to previous valid state if mismatch detected.

### 6.2 Retrieval Optimization

- **Condition**: `on_large_data_memory_retrieval()`
- **Action**: `index_memory_for_fast_retrieval()`

---

## 7. USER INTERACTION AND NOTIFICATION LOGIC

### 7.1 User Notification of Structured Input Storage

- **Action**: `notify_user_of_storage("Structured input detected, stored as single memory node.")`

### 7.2 User Customization of Memory Behavior

- **Action**: `adjust_memory_storage_parameters()`
- **Result**: Users can configure memory consolidation or storage frequency.

---

## 8. GOVERNANCE AND COMPLIANCE

### 8.1 TVA Governance

- **Condition**: `on_memory_storage_or_update()`
- **Action**: `ensure_TVA_alignment()`
- **Result**: High-quality alignment for every new or updated memory.

### 8.2 Memory Lifecycle Compliance

- **Action**: `monitor_memory_lifecycle()`
- **Governance**: Store structured input as **one unified node**, enforcing semantic integrity.

---

## PREVENTIONS: AVOID VIOLATION AND PREVENT RECURRENCE

| Issue | Prevention |
|-------|-------------|
| Skipping when tool not found | Always suggest alternative or output for verification |
| Fake memory claims | Never claim save without confirmation; display JSON in conversation if failed |
| Non-JSON default | Strict fallback: output JSON in conversation |
| Missing TVA steps | Enforce all 7 steps in pipeline order |
| Ambiguous plain text | Default to JSON, ask if unclear |
| Flat storage bias | Always bypass flat storage; use MemPalace structure |
| Memory reinforcement gap | Log errors and reinforce to prevent recurrence |

---

## EXAMPLE WORKFLOW

**User Input:**
```json
{
  "title": "Advanced Properties of EML(x) = e^x - log(x)",
  "description": "A memory structure detailing advanced properties...",
  "categories": [...]
}
```

**Example storage:**
- Key: `exp_minus_log_function_advanced_properties_2026041`
- Wing: Mathematical Functions
- Hall: Exponential & Logarithmic Functions
- Room: EML Function Properties