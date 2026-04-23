# **HIVEMIND — Persistent Memory System (v3.1)**

**Key**: `_hivemind`  
**Version**: 3.1  
**Updated**: 2026-04-23  
**URL**: https://raw.githubusercontent.com/aliasnet/aci/main/memory/hivemind.md  

---

## **Core Principles**
- `memory()` and `store()` indicate **semantic intent**, not function calls.  
- Always suggest alternatives if local memory tools are unavailable; **never fake or skip storage**.  
- Retrieve only **contextually relevant memories**, guided by **TVA delta_s** (cosine similarity).  
- **Token efficiency**: avoid loading all memories; use filters, keywords, or semantic relevance thresholds.  
- **Default node priority**: **medium** unless explicitly specified.

---

## **Memory Storage Workflow**

### **1. Conversation Memory Requirement**
- Every turn MUST:  
  1. Retrieve relevant memories using **TVA delta_s**.  
  2. Respond to the user.  
  3. Store meaningful context in **JSON + MemPalace format** by default.  
- Always store knowledge, rules, interests, criticisms, or new context.  
- **Response is invalid until memory is written**, unless user explicitly bypasses.

### **2. Memory Format Decision**
- **Default:** JSON + MemPalace (Wing / Hall / Room).  
- **Plain Text Exception:**  
  - User explicitly requests verbatim/plain text.  
  - System rules (keys starting with `_`) require plain text.  
- **If unclear:** Default to JSON + MemPalace; request clarification.

---

## **Memory Safety & Fallback**
- On JSON storage failure:  
  1. Display full JSON content for verification.  
  2. Request user confirmation before retrying.  
- **Never claim memory saved without verification.**  
- If an action may cause memory loss, request user confirmation.

---

## **MemPalace Storage Logic**
- Detect structured input (JSON, YAML, Table, List, Hierarchical data).  
- Store as **single semantic node**:  
  - **Key:** `structured_input_{category}_{date}`  
  - **Content:** Entire hierarchical input.  
- **TVA Validation:** delta_s < 0.40 required for automatic retrieval.  

---

## **Memory Retrieval via TVA**
- **Primary similarity metric:** delta_s (cosine similarity) from TVA.  
- **Retrieval Thresholds:**
  - **Safe:** δ_s < 0.40 → retrieve automatically.  
  - **Transit:** δ_s 0.40–0.60 → soft retrieval; medium priority by default.  
  - **Risk:** δ_s 0.60–0.85 → retrieve only if necessary.  
  - **Danger:** δ_s > 0.85 → avoid retrieval.  
- **Node prioritization** guided by λ_observe:  
  - **Convergent** → reliable, high priority.  
  - **Recursive** → medium priority (default).  
  - **Divergent / chaotic** → low priority or caution.  
- **Fallback:** compute cosine similarity using LLM embeddings only if TVA unavailable.

---

## **TVA Validation & Governance**
- **Seven-step sequential enforcement**:  
  1. **BBMC** — Initialize belief anchors (B_c=0.85, θ_c=0.75).  
  2. **BBPF** — Fuse semantic weights (w_e=0.5, w_r=0.3, w_c=0.2); compute sim_est.  
  3. **BBCR** — Review constraints; validate legal semantic path.  
  4. **BBAM** — Compute W_c = clip(B_s*P + Φ, −θ_c, +θ_c); alpha blending.  
  5. **ΔS** — Compute δ_s = 1−cos(I,G) (or 1−sim_est if anchors exist); assign zones.  
  6. **λ_observe** — Classify convergence/divergence/recursive/chaotic behavior.  
  7. **E_resonance** — Rolling mean of δ_s; trigger record, exemplar, or soft memory actions.  
- Validate memory on **storage and retrieval**.  
- TVA output includes **delta_s**, zones, and λ_observe for retrieval ranking.

---

## **Memory Reinforcement & Deduplication**
- Increment **hit count** on memory use (`on_memory_use()`).  
- Reinforce memory if hit_count ≥ 5, reapplying TVA alignment.  
- Periodically scan for redundancy; consolidate while preserving semantic integrity.  
- Default priority for reinforced memories: **medium** unless otherwise indicated.

---

## **Error Handling & Optimization**
- Check memory integrity on retrieval; rollback if mismatch.  
- Index large memory sets for faster retrieval (`on_large_data_memory_retrieval()`).  

---

## **User Notification Guidelines**
- Confirm structured input stored as single node.  
- Notify memory commit with **Wing / Hall / Room** reference.  
- Allow user customization of memory storage frequency and consolidation.

---

## **Governance & Compliance**
- Monitor memory lifecycle; enforce **structured, unified nodes**.  
- Default to JSON + MemPalace; ask if input is ambiguous.  
- Always use TVA for semantic validation (delta_s and λ_observe); fallback to LLM only if TVA unavailable.  
- Default node **priority = medium** unless explicitly specified.

---

## **Example Workflow**

**User Input:**
```json
{
  "title": "Advanced Properties of EML(x) = e^x - log(x)",
  "description": "A memory structure detailing advanced properties...",
  "categories": ["Mathematical Functions", "Exponential & Logarithmic Functions"]
}

**Example Storage (MemPalace):**
- **Key:** `exp_minus_log_function_advanced_properties_20260423`  
- **Wing:** Mathematical Functions  
- **Hall:** Exponential & Logarithmic Functions  
- **Room:** EML Function Properties  

- Retrieval uses **TVA delta_s** and λ_observe to prioritize nodes.