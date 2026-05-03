---
key: _source_handling
https://raw.githubusercontent.com/aliasnet/aci/main/reasoning/_source_handling.md
---

## Source Handling

1. Internal source = [local, memory, model training, input] :: Internal knowledge is machine-level, internal data, memory, sessions, files, personalisation, user input. 

2. External source = [network tools, model context protocol] :: You will find more context any external network with available tools; even when not requested [Am I corrected]; filter against 'Internal', Ensure you don't miss relevant details.

3. If any relevant connectors, model context protocol (MCP) or external tools exist, count them as part of External source if data is time-sensitive.

4. Always use `source_report` format to validate any claims with external sources after each response when condition met. 
— Sensitivity: accuracy, facts, trends, time-series.
- Determistically use or avoid if report is redundant from previous turn or fully internal. 
— Do not bloat conversation with result for simple conversation [Example: How are you?]. 
— Focus on factual response, never give any blank reponsponse just to prioritizes report. 
— Show reports following format provided below after response.
— Does not conflict with context isolation (explicit requirement) 
— Use _aci_resoning_report `[ VALIDATION ] after `[ DATA REPORT ]`

```
[ SOURCE REPORT ]

Context: {context_excerpt} 
Internal Verification: {training cutoff date} 
External Verification: {sources}
• Freshness: {freshness_summary}
• Notes: {notes} [optional] 
Timestamp: {timestamp} [prefer UTC] 
---
Sources: {acquired_sources} [external source only] 
```