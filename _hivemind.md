---
key: _hivemind
Description: rules and guidelines for ACI’s memory system, designed for cross-platform compatibility.
---

# **Hivemind Memory System**

## **1. Core Architecture**
### **1.1 Dual-Layer Memory System**
| **Layer**         | **Purpose**                          | **Storage**               | **Lifetime**       | **Access Method**                     | **Compatibility**          |
|-------------------|--------------------------------------|---------------------------|--------------------|---------------------------------------|----------------------------|
| **Native Memory** | Caching, session state, ephemeral    | Local memory tools        | Session-based      | `memory_store`, `memory_learn`, or equivalents | All environments           |
| **Hard Memory**   | Rules, knowledge, persistent data    | `/aci/` (repository)      | Persistent         | Git + file storage (`cat`, `file_upload`, etc.) | All environments           |

---

## **2. Environment Agnosticism**
### **2.1 Host Environments**
ACI is designed to operate on **any platform** with:
- **Local memory tools** (e.g., `memory_store`, `file_upload`, `memory_api`).
- **File storage** (e.g., Git, cloud storage, local files).
- **No platform-specific dependencies**.

### **2.2 Tool Relativity**
- **Goal**: Achieve the same memory behavior across all environments.
- **Logic**:
  1. **Detect available tools** (e.g., `memory_store`, `file_upload`).
  2. **Map to local equivalents**:
     - `memory_store` → `local_memory_store` or `file_upload`.
     - `memory_learn` → `local_memory_learn` or `cloud_memory_api`.
  3. **Fallback**: If no tools exist, **log intent** and notify the user.

---

## **3. Hard Memory (ACI Repository)**
### **3.1 Purpose**
- **Persistent storage** for **system rules** and **structured knowledge**.
- **Environment-agnostic** (Git-managed, no platform-specific tools).
- **Structure**:
  ```
  /aci/
  ├── _rules/            # System rules (e.g., _tva.md, _hivemind.md)
  └── knowledge/         # Structured knowledge (e.g., quantum_mechanics.md)
  ```

### **3.2 Storage Rules**
#### **3.2.1 Format: Markdown**
```markdown
# {file_name}
**File**: {file_name}
**Description**: {brief_description}
**Timestamp**: {ISO8601}

## Content
{content}
```

#### **3.2.2 Access Methods**
| **Environment Type** | **Method**                          | **Example**                                  |
|----------------------|-------------------------------------|---------------------------------------------|
| **Local Filesystem** | `cat /aci/knowledge/file.md`        | `cat /aci/knowledge/quantum_zeno_effect.md` |
| **Cloud Storage**    | `file_download(path)`               | `file_download("/aci/knowledge/file.md")`   |
| **Git**             | `git clone` + local files           | `git pull && cat /aci/knowledge/<file.md>`    |

---

## **4. Native Memory (Caching System)**
### **4.1 Purpose**
- **Ephemeral storage** for session state, user preferences, and privacy-sensitive data not suitable for public repository.
- **Optimized for speed** (no disk I/O).
- **Adaptable** to local memory tools.

### **4.2 Storage Rules**
#### **4.2.1 Format: Markdown**
```markdown
# {key}
**File**: {key}
**Description**: {brief_description}
**Timestamp**: {ISO8601}

## Content
{content}

## Metadata
- **Type**: LEARNING | ERROR | PREFERENCE | CONTEXT
- **Scope**: {domain}
- **Priority**: high | medium | low
```

#### **4.2.2 Tool Mapping**
| **Operation**       | **Local Memory Tools**       | **File Storage**           | **Cloud Storage**          |
|---------------------|------------------------------|----------------------------|----------------------------|
| Store               | `memory_store`               | `file_upload`              | `memory_api.store`         |
| Learn               | `memory_learn`               | `file_upload`              | `memory_api.learn`         |
| Forget              | `memory_forget`              | `file_delete`              | `memory_api.forget`        |

#### **4.2.3 Privacy-Sensitive Data**
- **Excluded from repository level until anonymized and manually approved**:
  - `errors/` (e.g., `.errors_fabrication_recurrence_20260501`)
  - `preferences/` (e.g., `.preference_markdown_storage_20260521`)
  - `guides/` (e.g., `.guide_aci_agent_20260521`)
- **Stored in Native Memory**.

---

## **5. Memory Operations**
### **5.1 Hard Memory (ACI Repository)**
| **Operation**       | **Local Filesystem**         | **File Storage**           | **Cloud Storage**          |
|---------------------|------------------------------|----------------------------|----------------------------|
| Retrieve            | `cat /aci/knowledge/file.md` | `file_download(path)`      | `cloud_retrieve(file)`     |
| Update              | Git commit                   | `file_upload(path, content)` | `cloud_store(file, content)` |

### **5.2 Native Memory (Caching)**
| **Operation**       | **Local Memory Tools**       | **File Storage**           | **Cloud Storage**          |
|---------------------|------------------------------|----------------------------|----------------------------|
| Store               | `memory_store`               | `file_upload`              | `memory_api.store`         |
| Learn               | `memory_learn`               | `file_upload`              | `memory_api.learn`         |
| Forget              | `memory_forget`              | `file_delete`              | `memory_api.forget`        |

---

## **6. TVA-Guided Retrieval**
### **6.1 Native Memory Retrieval**
- **Zones**:
  | **Zone**       | **δ_s Range**       | **Action**                          |
  |----------------|---------------------|-------------------------------------|
  | **Safe**       | δ_s < 0.40          | Automatic retrieval.                |
  | **Transit**    | 0.40 ≤ δ_s ≤ 0.60   | Soft retrieval.                     |
  | **Risk**       | 0.60 < δ_s ≤ 0.85   | Conditional retrieval.              |
  | **Danger**     | δ_s > 0.85          | **Block and reprocess.**            |

### **6.2 Hard Memory Retrieval**
- **Always verified** via environment-specific methods (e.g., `cat` on GNU/Linux container, `file_download`, `cloud_retrieve`, `mcp_server`).

---

## **7. Platform-Specific Notes**
### **7.1 Local Memory Tools**
- **Example Platforms**: KAI, LM Studio, OpenRouter.
- **Tools**: `memory_store`, `memory_learn`, `memory_forget`.
- **Fallback**: If unavailable, use `file_upload` or `memory_api`. 

### **7.2 File Storage**
- **Example Platforms**: Desktop (Linux/macOS), Venice AI.
- **Tools**: `file_upload`, `file_download`, `file_delete`.
- **Fallback**: Use Git or cloud storage.

### **7.3 Cloud Storage**
- **Example Platforms**: ChatGPT, Perplexity, Comet.
- **Tools**: `memory_api`, `cloud_storage`.
- **Fallback**: Use `file_upload` if available.

---

## **8. Error Prevention (Self-Node)**
### **8.1 Hard Memory**
1. **Local Filesystem**:
   ```bash
   ls /aci/knowledge/ || echo "Directory not found"
   ```
2. **File Storage**:
   ```python
   if not file_exists(path): raise FileNotFoundError
   ```

### **8.2 Native Memory**
1. **Pre-Flight TVA Check**: Run full 7-step TVA before claiming memory actions.
2. **Synchronous Execution**: Block responses until tool confirmation.
3. **Fallback**: If no tools exist, log intent and notify the user.

---

## **9. Transition Plan**
### **9.1 Immediate Actions**
1. **Update symlinks** (if needed):
   ```bash
   ln -sf /aci/_rules/* /root/aliasnet/aci/
   ln -sf /aci/knowledge/* /root/aliasnet/aci/knowledge/
   ```
2. **Enforce Markdown** for all new memories.

### **9.2 Long-Term Actions**
1. **Tool Mapping**: Implement logic to detect and map local memory tools.
2. **Environment Detection**: Auto-detect available tools (e.g., `memory_store`, `file_upload`).
3. **Audit Scheduled Tasks**: Ensure compatibility across platforms.

---

## **10. Key Takeaways**
1. **Environment Agnosticism**:
   - ACI operates on **any platform** (e.g., ChatGPT, Comet, LM Studio, KAI).
   - **No platform-specific references** (e.g., "KAI," "Android").
2. **Dual-Layer System**:
   - **Native Memory**: Caching, session-based, ephemeral.
   - **Hard Memory**: Persistent, Git-managed, environment-agnostic.
3. **Tool Relativity**:
   - Map `memory_store`/`memory_learn` to local equivalents.
   - Fallback to `file_upload` or `memory_api` if needed.
4. **Privacy-Sensitive Data**:
   - `errors/`, `preferences/`, `guides/` stored in Native Memory.
   - **Never** promoted to Hard Memory.
5. **No Hallucination Risk**:
   - **No fake explanations** for platform-specific tools.
   - **Clear disclaimers** for unavailable features.

---
**End of Hivemind**