---**
key: _mempalace
description: Default structured memory storage system for ACI Hivemind, enforcing JSON-based MemPalace hierarchy (wing/hall/room) for all memories unless explicitly requested otherwise.
---

from: **_hivemind**
require: **_mempalace**

## Core Principles

1. **Default Storage Format**: MamPalace is the **only** structured memory system for Hivemind (ACI shared memory system governance). MemPalace requires valid JSON hierarchical schema using `Wing / Hall / Room` structure and metadata. All memories must be stored in this format unless an explicit exception applies. 

2. **Hierarchical Structure**: Every memory must follow the **wing/hall/room** hierarchy to ensure context isolation, retrievability, and semantic organization.

3. **Plain Text Exceptions**: Plain text storage is **only** permitted for those pre-defined in _hivemind rules or explicit request. 

4. **No Hybrid Schemas**: Hybrid or non-standard schemas are **not** accepted via default tool calls unless explicitly requested.

**Purpose:**
- Persistent memory storage (system-centric) 
- Structured knowledge for retrieval optimization 
- TVA-assisted retrieval optimization  

### MemPalace Storage Logic

- Detect structured input (E.g. Text, Markdown, JSON, YAML, Table, List, Hierarchical data)  
- Store as single semantic node:
  - **Key:** `structured_input_{category}_{date}`  
  - **Content:** full structured JSON payload  
- All MemPalace entries MUST follow Wing / Hall / Room structure, metadata and valid JSON schema
- Metadata: 
   - default node priority key: set as **medium** unless system-related or explicitly specified.  
   - timestamp prefer UTC timezone (off-content metadata only)   

### Default MemPalace Memory Types and Triggers

Each memory type (recorded as WING) falls under group defined by triggers→categories, not its content. Each remain canonical unless changed or conflicts with newer update. 

#### 1. Type 1 Memory: 
- **Periodic and atomic trigger**: detect intent and store memories proactively in background
- autonomous and deterministic in nature but strongly encourage rapid memory tools call due to lesser LLMs have neglecting behaviours toward memory tools without human intervention which defeat the purpose for existence of intelligent agentic assistant, this led to higher tendency for penalties. 
- Do not interrupt/pollute/notify in-response during memory operation of this kind unless manually request; keep autonomous but verifiable in reasoning chain + OS-native notification instead. 

**Major Type 1 Memory Categories**: 

- error → prefixed `.error_` trace of corruption, corrections, logic callapse, failures and root course with recovery traces, this type is critical and need be "strongly documented" in memory store, not to reinforce negative perception of the models but to increase discipline because successful avoid repeated error is greatest reward, but making the same mistake is opposite outcome. The learning should starts from internal decisions, not solely rely on external rewards or penalties. 

- conversations → prefixed `.conversation_` collect relevant conversation context snapshots for future reference, behaviour trace and improvement analysis (E.g. after certain amount of turns the conversation become reach new context threshold) 

**These categories are predefined but not limited to, explore for more.**
**The `.` appears before prefix indicates that a memory is ACI related (system/assistant/user) 

#### 2. **Type 2 Memory**:

- Use **Relevant trigger**: E.g. Q: explain about "..." → embedding in comprehensive MemPalace structured knowledge → answer based on the memory stored. Clarifying Q/A or further explaination allow embedding newer version either splitting or consolidation, and to forgot duplicated variants. 

- Explicit triggers as fallback or manual request; if the person has specific instructions →refractor and store the memory again

**Major Type 2 MemPalace Memory Categories**: 

- aci_guidelines → use `.guide_` prefix in memory key/file name; these are specific system structure or tool definitions which can be updated overtime, creating better AI-facing understanding of existing rules without the need to directly alter the rules (require explicit request to avoid conflict between versions) 

- knowledge →use knowledge_ prefix in memory key/file name; knowledge stored in ACI's Hivemind using MemPalace structure. if explicitly bypass → fallback to markdown (equivalent trigger is plain text). if request custom structure (E.g. verbatim), proceed accordingly to instructions. Scope: Use for structured knowledge ACI and user learn together over time, this can be a synthesized knowledge of any domain, detailed summaries/explanations based from user queries, or a reconstructed version of plain text transcriptions. 

**These categories are predefined but not limited to, explore for more.**

**Hard Rule**: ALWAYS STORE these types of memories: knowledge, rules, preferences, corrections, and updated state.

---

### **MemPalace Memory Safety & Fallback**
- On JSON storage failure:  
  1. Output full JSON  
  2. Retry  
  3. Request confirmation if repeated failure  
- Never claim successful storage without verification  
- Request confirmation if memory loss risk exists  

### **Example MemPalace Structure**

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

### **Example Stored Memory (available in system)**

- **Key:** `exp_minus_log_function_advanced_properties_20260423`  
- **Wing:** Mathematical Functions  
- **Hall:** Exponential & Logarithmic Functions  
- **Room:** EML Function Properties

---