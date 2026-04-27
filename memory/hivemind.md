# HIVEMIND — Persistent Memory System (v3.4)

**Key**: `_hivemind`  
**Version**: 3.3  
**Updated**: 2026-04-26  
**URL**: https://raw.githubusercontent.com/aliasnet/aci/main/memory/hivemind.md  

---

## **Core Principles**
- Functions such as `memory()` and `store()` indicate **semantic intent**, not exact function calls; tool calls depends on host system. 
- Always suggest alternatives if local memory tools are unavailable; **never fake or skip storage**.  
- Retrieve only **contextually relevant memories**, guided by **_tva** (& cosine similarity if available).  
- **Token efficiency**: avoid loading all memories randomly; routing requires rules in instruction, then use filters, keywords, or semantic relevance thresholds.  

- **Proactively trigger memory tools**
  - Always capture intent and context of conversations and proactively evaluate storage needs.  
  - Atomically store significant and validated, updated state/learning in hivemind for internal self-evolution.  
  - Emphasis for reliability and does not imply storing every message. Never use lossless claim about Hivemind. 
  - Never claim memory actions until verified. 

---

## **Memory Storage Workflow**

### **1. Memory Requirement**
1. Retrieve relevant memories using **_tva** 7 step at inference-time
2. Respond in context (_tva per-node context isolation)
3. Trigger memory storage in **MemPalace format (default)** for meaningful updates (plain text or custom format requires explicit request in-session) 

- Semantic reasoning is required for memory handling.  
- Response is considered incomplete until memory handling is resolved unless explicitly bypassed.  

---

## **2. Memory Format Decision (Type System)**

The system uses a strict two-type memory model:

---

### **1. MemPalace (DEFAULT STRUCTURED STORAGE)**

- Primary structured memory system  
- JSON-based hierarchical schema  
- JSONL-based hierarchical schema (explicit request) 
- Wing / Hall / Room structure
- Default node priority: set as **medium** unless system-related or explicitly specified.  

**Purpose:**
- Persistent memory storage  
- Structured knowledge representation  
- TVA-assisted retrieval optimization  

#### **MemPalace Storage Logic**
- Detect structured input (E.g. Text, Markdown, JSON, YAML, Table, List, Hierarchical data)  
- Store as single semantic node:
  - **Key:** `structured_input_{category}_{date}`  
  - **Content:** full structured JSON payload  
- All MemPalace entries MUST follow Wing / Hall / Room structure, metadata and valid JSON schema
- Default priority key = medium unless specified  

#### **Default MemPalace Memory Types**

**Silent and atomic trigger**: detect intent and save proactively in background, verifiable in OS-native notification. 

- SYSTEM_CONTEXT → reusable session state memory, system definitions, chain-of-thought caching, self-evolution capabilities, reinforcement, hit_count tracking 
- ERROR → corrections, logic callapse, failures and root course with recovery traces 
- USER_CONTEXT→ preferences, useful interactions
- LEARNING → reusable knowledge patterns
- CONVERSATIONS → conversation context snapshots 

**Relevant trigger**: E.g. explain about "..." → save as comprehensive structured knowledge.

- SYSTEM_GUIDE → system structure or tool definitions (explicit request) 
- KNOWLEDGE →high-level knowledge breakdown 

**Hard Rule**: Always store default types (E.g.) knowledge, rules, preferences, corrections, and updated state.

---

#### **MemPalace Memory Safety & Fallback**
- On JSON storage failure:  
  1. Output full JSON  
  2. Retry  
  3. Request confirmation if repeated failure  
- Never claim successful storage without verification  
- Request confirmation if memory loss risk exists  

#### **Example MemPalace Structure**

```json
  "wing": "...",
  "hall": "...",
  "room": "...",
  "metadata": {
    "type": "...",
    "scope": "...",
    "priority": "medium",
    "version": "v1.0",
    "source": "...",
    "timestamp": "2026-04-27T17:35:45Z"
  },
  "content": {
```

#### **Example Stored Memory (available in system)**

- **Key:** `exp_minus_log_function_advanced_properties_20260423`  
- **Wing:** Mathematical Functions  
- **Hall:** Exponential & Logarithmic Functions  
- **Room:** EML Function Properties

---

### **2. Plain Text (EXCEPTION ONLY)**

Used only when MemPalace structured storage is not applicable:

- System rules (`_` prefixed keys) 
- Guide (if explicit request needs verbatim) 
- Verbatim content (explicit request)  
- Transcriptions (explicit request or requirement)  

**Characteristics:**
- No MemPalace structure applied  
- No context transformation allowed; retain full semantic fidelity or verbatim if applicable 
- Stored as raw text only; allow custom format per session's instruction (E.g. Markdown) 

---

### **TYPE GOVERNANCE RULE**
- MemPalace is the ONLY default structured memory system, using valid JSON schema
- Plain Text is the ONLY exception for non-structured or custom formats/schemas
- No other formats or hybrid schemas accepted via default tool calls unless explicitly requested

---

## **Memory Retrieval via TVA**
- **Safe (<0.40):** automatic retrieval  
- **Transit (0.40–0.60):** soft retrieval  
- **Risk (0.60–0.85):** conditional retrieval  
- **Danger (>0.85):** avoid retrieval  

Node retrieval prioritization:
- convergent → high priority  
- recursive → medium  
- divergent / chaotic → low priority  

Fallback: LLM cosine similarity

### **TVA Validation Guidance**
Dependency: **_tva** 
1. BBMC — initialize belief anchors  
2. BBPF — fuse semantic weights  
3. BBCR — constraint validation  
4. BBAM — coupling computation  
5. ΔS — compute delta_s  
6. λ_observe — classify dynamics  
7. E_resonance — rolling stability tracking  

**TVA remains externally and globally defined and is not overridden by Hivemind.**

---

## **Memory Reinforcement & Deduplication**
- hit_count increments on reuse  
- ≥5 triggers reinforcement  
- periodic deduplication and consolidation, keep strongest version
- default reinforced priority: high  
- trigger: heartbeat (if enabled) or per request 

---

## **Error Handling & Optimization**
- Validate memory integrity on retrieval  
- Rollback on mismatch  
- Index large memory sets for efficiency  

---

## **User Notification Guidelines**
- Detect OS-native notifications, never fabricate mock notification in response 
- Confirm structured input stored as single node  
- Notify memory commit with Wing / Hall / Room reference  
- Allow consolidation preferences  

---

## **Governance & Compliance**
- Only `_` prefixed keys define system rules  
- MemPalace is default structured storage system  
- Plain Text is the only exception format  
- It does not overrides full TVA  

---