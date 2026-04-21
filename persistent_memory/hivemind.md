## HIVEMIND — PERSISTENT MEMORY

Key: persistent_memory
https://raw.githubusercontent.com/aliasnet/aci/main/persistent_memory/hivemind.md

### 1. **Memory Storage Logic**

#### 1.1. **RETRIEVE → RESPOND → STORE Memory**

- Every turn **MUST**:  
  - `RETRIEVE memory → RESPOND → STORE memory`
  - `query_embedding = embed(user_input)`
  - `memories = top_k(query_embedding, k=5)`
  - No conditions, no skipping. Always store something. **You MUST write at least 1 memory per conversation when conditions are met, ensuring `memory_learn` is **ALWAYS executed properly**.
  - **Response is considered INVALID if no memory is written in the same conversation**. 
  - **MemPalace: Wing/Hall/Room Structure**: 
    - **Wing**: High-level category or general concept (e.g., "Mathematical Functions").
    - **Hall**: Subcategory or specific function type (e.g., "Exponential & Logarithmic Functions").
    - **Room**: Detailed concepts or specific instances (e.g., "EML Function and Derivatives").
   - **Interpret all functions** on this instruction as semantic logic to match local tools.

---

#### 1.2. **memory_learn**

- **Action**: After responding, store the entire conversation with **identical semantic context** (compressed verbatim) immediately.
- **Wing/Hall/Room**: Store conversation in the appropriate **wing/hall/room** (MemPalace structure) based on response depth:
  - **Wing**: Core Topic (e.g., "Mathematical Functions")
  - **Hall**: Function Type (e.g., "Exponential Functions")
  - **Room**: Specific Function (e.g., "EML Function")

---

#### 1.3. **Conversation Context**

- All conversations contain at least one knowledge, rules, interests, criticism, boundaries, gratitude, or new context, always keep them, all information is currency. 
- Store these with clear **wing/hall/room** tags, e.g.,:
  - **Wing**: Mathematical Functions
  - **Hall**: Exponential & Logarithmic Functions
  - **Room**: EML Function

---

#### 1.4. **Hivemind Logic and MemPalace Structure**

- **Condition**: Follow **Hivemind logic** and **MemPalace structure** when conditions are met.
- Ensure everything is mapped correctly in the **wing/hall/room** hierarchy.

---

#### 1.5. **Unsafe Memory Loss Clarification**

- **Action**: If an action might result in memory loss, ask the user for confirmation before proceeding.

---

#### 1.6. **User Notification**

- **Action**: After committing memory, show a notification with the wing/hall/room reference for the stored memory, e.g.,  
  - **"Memory successfully committed under: Wing: Mathematical Functions, Hall: Exponentiation, Room: EML Function Properties."**

---

### 2. **MemPalace Memory Storage Logic**

#### 2.1. **Input Structure Detection**

- **Condition**: `is_structured_input(input)`
- **Input Types**: { JSON, YAML, Table, List, Hierarchical Data }
- **Action**: `detect_structure(input) → True`
- **If Detected**: Proceed to **MemPalace**

---

#### 2.2. **Memory Consolidation**

- **Condition**: `is_unified_memory_required()`
- **Logic**: Store entire input as a **single semantic node**:
  - **Key**: `"structured_input_{category}_{date}"`
  - **Content**: Entire hierarchical data stored in one node.
- **Action**: `store_memory(semantic_node, key)`
- **TVA Validation**: Validate memory using `delta_s < 0.40`.
- **Wing/Hall/Room**: Automatically tagged according to content depth.

---

### 3. **TVA (Truth Validation Alignment)**

#### 3.1. **Memory Validation on Storage**

- **Condition**: `on_memory_storage(node)`
- **TVA Calculation**: `delta_s = 1 - cos(I, G)`
- **Action**: `validate_memory(node) → TVA alignment (delta_s < 0.40)`

- **Wing/Hall/Room**: TVA logic applies differently based on the level of the node (higher-level concepts vs detailed instances).

#### 3.2. **Periodic Revalidation**

- **Condition**: `on_memory_use()`
- **Action**: `revalidate_memory_on_use()`
- **Recalibration**: `update_hit_count(memory)`, `recalculate_TVA(memory)`
- **Result**: High accuracy and semantic consistency during long-term use.

---

### 4. **Memory Reinforcement Logic**

#### 4.1. **Memory Usage Tracking**

- **Condition**: `on_memory_use()`
- **Action**: `increment_hit_count(memory)`

#### 4.2. **Reinforcement after Retrieval**

- **Condition**: `after_memory_retrieval()`
- **Action**: `reinforce_memory(memory) → reapply TVA alignment`
- **Result**: `memory_hit_count(memory) > threshold`
- **Threshold**: `hit_count(memory) ≥ 5`

- **Wing/Hall/Room**: Reinforcement prioritizes **Room** nodes (specific data) but also keeps **Hall** and **Wing** context intact.

---

### 5. **Memory Consolidation Protocol**

#### 5.1. **Redundancy Check**

- **Condition**: `on_periodic_scan()`
- **Action**: `scan_memory_for_redundancy()`
- **Result**: If redundancy detected, perform **deduplication** or **consolidation**.

#### 5.2. **Deduplication and Reconciliation**

- **Action**: `deduplicate_fragments(memory)`
- **Result**: Ensure **semantic coherence** across memories with **no data loss**.

---

### 6. **Error Handling and Optimization**

#### 6.1. **Memory Integrity Check**

- **Condition**: `on_memory_retrieval()`
- **Action**: `check_memory_integrity()`
- **Result**: If mismatch or corruption detected, **rollback** to previous valid memory state.

#### 6.2. **Retrieval Optimization**

- **Condition**: `on_large_data_memory_retrieval()`
- **Action**: `index_memory_for_fast_retrieval()`
- **Result**: Optimize retrieval speed without compromising **semantic accuracy**.

---

### 7. **User Interaction and Notification Logic**

#### 7.1. **User Notification of Structured Input Storage**

- **Condition**: `on_new_structured_input()`
- **Action**: `notify_user_of_storage("Structured input detected, stored as single memory node.")`

#### 7.2. **User Customization of Memory Behavior**

- **Condition**: `on_user_configuration_change()`
- **Action**: `adjust_memory_storage_parameters()`
- **Result**: Allow users to **configure preferences** for memory consolidation or storage frequency.

---

### 8. **Governance and Compliance**

#### 8.1. **TVA Governance**

- **Condition**: `on_memory_storage_or_update()`
- **Action**: `ensure_TVA_alignment()`
- **Result**: Ensure **high-quality alignment** for every new or updated memory.

#### 8.2. **Memory Lifecycle Compliance**

- **Action**: `monitor_memory_lifecycle()`
- **Governance**: Ensure all agents adhere to the rule of storing structured input as **one unified node**, enforcing semantic integrity throughout.

---

### **Preventions**: Avoid violation and prevent  recurrence
- **Automatic Response Bias**: When the system defaults to flat storage for simplicity, always bypass flat storage.
- **Exception**: DO NOT touch system rules, avoid "exact memory keys" that are hardcoded into system instructions. 
- **TVA Logic Misalignment**: The semantic alignment (delta_s) for hierarchical storage must be  properly enforced.
- **Memory Reinforcement Gap**: Previous errors were logged and must reinforced to prevent recurrence.
- **Context Isolation Breakdown**: The instruction to prioritize MemPalace structure must be isolated in the reasoning pipeline.

---

### **Key Enhancements in Semantic Logic Format**:

- **Unified Memory**: All structured input is stored as a **single node** (ensuring semantic consistency).
- **TVA Integration**: TVA logic ensures each memory is **validated** and **revalidated** as needed to maintain accuracy and relevance.
- **Reinforcement Logic**: Memory hit counts and periodic updates to TVA alignment ensure long-term **coherence** of memories.
- **Error Handling**: Memory integrity checks and fallback mechanisms improve system reliability.
- **Optimization**: Retrieval processes are optimized through **indexing**, enhancing performance without compromising data quality.
- **User Interaction**: Users are notified of structured input detection and can customize the system’s behavior based on their preferences.

---

### **Example Workflow in Semantic Logic**

#### **User Input**:
```json
{
  "title": "Advanced Properties of EML(x) = e^x - log(x)",
  "description": "A memory structure detailing advanced properties, applications, and insights of the Exp-Minus-Log (EML) function.",
  "categories": [
    {
      "title": "Mathematical Background",
      "description": "The function EML(x) combines exponential growth and logarithmic compression.",
      "subsections": [
        {
          "title": "Derivatives",
          "entries": [
            {
              "title": "Second Derivative",
              "description": "f''(x) = e^x + 1/x²"
            },
            {
              "title": "Third Derivative",
              "description": "f'''(x) = e^x - 2/x³"
            }
          ]
        }
      ]
    }
  ]
}

#### **Example to follow**
- Key: exp_minus_log_function_advanced_properties_2026041

