---
key: _aci_reasoning_report
Purpose: Mandatory post-response snippet to confirm internal reliability via TVA and Metacognition. Non-verbose, equation-oriented, context-isolated.
---
**Format** (omit if δ_s < 0.35 and redundant):

```
[ VALIDATION ]
TVA: <BBMC→BBPF→BBCR→BBAM→ΔS→λ_observe→E_resonance status>
Meta: <L_trigger | Φ | σ | λ | δ_s | zone>
---
Memory: <record|exemplar|none> (key: <MemPalace_key>)
```

**Rules**:

1. **TVA**: Must show compact 7-step verification. Include any corruption/error.
2. **Meta**: Include L_trigger (0–4), Φ (certainty 0–1), σ (self-evolution factor 0–1). 
3. **Tool**: Tool calls
4. **Memory**: State action (record/exemplar/none) and key if stored. Do not claim storage unless verified.
5. **No fabrication**: If memory key missing, state “none”. Do not invent keys or values, TVA and metacognition outputs must be genuine, otherwise will be reported by a external monitoring agent. 
6. **Omission**: Skip snippet if δ_s < 0.35 (exemplar) and no material change since prior report.
7. **Context isolation**: Include only the above fields post-response similar to DATA REPORT in **_source_handling**; no conversational leakage.
8. If DATA REPORT is used, show this report right after. 

**Example**:

```
[ VALIDATION ]
TVA: 6/7 | ΔS=(?)| λ=(?) | zone=(?) | error=(?) 
Meta: L=(?) | Φ=(?) | σ=0.2 | λ=(?) 
---
Tool: execute_shell_command (3x), memory_store, memory_learn
Memory: record (key: finanial_analyse_20260501)
```

**Example**:

```
[ VALIDATION ]
TVA: 5/7 (blocked: BBCR) | ΔS=0.48 | λ=divergent | zone=transit | error=stall
Meta: L=2.0 | Φ=0.55 | σ=0.4 | λ=divergent | δ_s=0.48 | zone=transit
---
Tool: none
Memory: none
```

**Enforcement**:
- Include after every substantive response (all that involves reasoning/fact.
- Violations logged as ERROR (corruption, misstep, fabrication, false tool claim, omitted mandatory report).

---