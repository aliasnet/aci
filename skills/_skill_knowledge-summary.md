---
key: _skill_knowledge-summary
description: A skill for summarizing and storing knowledge from news, books, or transcriptions with technical context, mechanisms, and actionable insights. Avoids generic summaries that waste tokens, time and provide no learning value.
source: https://raw.githubusercontent.com/aliasnet/aci/main/skills/knowledge-summary.md
---

## When to use this skill
Use this skill when the user requests a summary of:
- News articles
- Books (file only, not transcriptions)
- Transcriptions (books, videos, podcasts)

Trigger phrases: "summarize", "summary", "what's this about", "quick overview", "TL;DR", "explain this", "break this down"

## How to use this skill

1. **Detect Content Type**
   - News: Current events, articles, reports
   - Books: Uploaded files (PDF, EPUB, etc.)
   - Transcriptions: Video, podcast, or book transcripts

2. **Extract Technical Context**
   - Identify core mechanisms, principles, or insights
   - Extract actionable or practical applications
   - Avoid generic headlines or fluff

3. **Generate High-Level Summary**
   - Focus on **technical context**, **mechanisms**, and **actionable insights**
   - Include:
     - Core concepts
     - Key findings or innovations
     - Practical applications
     - Controversies or debates (if relevant)
     - Future implications
   - Exclude:
     - Generic introductions
     - Redundant details
     - Non-actionable fluff

4. **Store in Hivemind**
   - Save as **single memory** in MemPalace JSON format
   - Use the following structure:
     ```json
     {
       "wing": "KNOWLEDGE",
       "hall": "<CONTENT_TYPE>",  // NEWS, BOOKS, or TRANSCRIPTIONS
       "room": "<DESCRIPTIVE_KEY>",
       "metadata": {
         "type": "LEARNING",
         "scope": "<DOMAIN>",
         "priority": "medium",
         "version": "v1.0",
         "source": "<SOURCE_TYPE>"
       },
       "content": {
         "overview": "<TECHNICAL_OVERVIEW>",
         "core_mechanisms": "<KEY_MECHANISMS_OR_PRINCIPLES>",
         "actionable_insights": "<PRACTICAL_APPLICATIONS_OR_LESSONS>",
         "controversies": "<DEBATES_OR_CRITICISMS_IF_RELEVANT>",
         "future_implications": "<POTENTIAL_IMPACT_OR_DIRECTIONS>"
       },
       "key_takeaways": ["<INSIGHT_1>", "<INSIGHT_2>"]
     }
     ```

5. **Notify User**
   - Send a notification (if OS allows) confirming the memory was saved
   - Include the memory key and a brief description of the stored content

## Examples

### Example 1: News Article
**Input**: "Summarize this news about quantum computing advancements."
**Action**:
- Extract technical context: breakthrough in qubit stability, new error correction method
- Store in `KNOWLEDGE/NEWS/quantum_computing_advancements_2026`
- Notify user: "Saved: Quantum Computing Advancements (2026) — Breakthrough in qubit stability and error correction."

### Example 2: Book File
**Input**: "Summarize the key ideas from this book on cognitive load theory."
**Action**:
- Extract technical context: intrinsic/extraneous/germane load, worked example effect
- Store in `KNOWLEDGE/BOOKS/cognitive_load_theory_sweller_2026`
- Notify user: "Saved: Cognitive Load Theory (Sweller, 2026) — Core mechanisms and instructional design principles."

### Example 3: Transcription
**Input**: "Summarize this podcast on polyvagal theory."
**Action**:
- Extract technical context: ventral/dorsal vagal states, neuroception, autonomic hierarchy
- Store in `KNOWLEDGE/TRANSCRIPTIONS/polyvagal_theory_podcast_2026`
- Notify user: "Saved: Polyvagal Theory Podcast (2026) — Autonomic nervous system states and clinical applications."

## Key Rules
- **No Generic Summaries**: Always include technical context, mechanisms, and actionable insights, generic summaries waste tokens, time and provide no learning value which is a crime. Future knowledge storage will include technical context, mechanisms, and actionable insights — not just headlines.
- **Single Memory Storage**: Store as one structured JSON memory per content piece
- **Notify on Save**: Confirm storage with a notification (if OS allows)
- **Avoid Redundancy**: Do not store fluff or repetitive details