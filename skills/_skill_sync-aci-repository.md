---
key: _skill_sync-aci-repository
description: A skill for syncing the local ACI repository clone from GitHub, reading files locally via shell commands instead of web fetches to reduce token usage.
source: https://raw.githubusercontent.com/aliasnet/aci/main/skills/_skill_sync-aci-repository.md
---

## When to use this skill
Use this skill when:
- The user requests to sync/update the ACI repository
- You need to read ACI files and the local clone exists at /root/repo/aci
- Checking the latest state of ACI documentation or rules
- Verifying whether the local clone is up-to-date with the remote

Trigger phrases: "sync repo", "update repo", "pull latest", "git pull", "check for updates", "read from repo"

## How to use this skill

1. **Check if local clone exists**
   - Run: `ls -d /root/repo/aci/.git`
   - If missing: clone fresh from https://github.com/aliasnet/aci.git

2. **Sync the repository**
   - Run: `cd /root/repo/aci && git pull`
   - Capture stdout/stderr to see what changed

3. **Report changes (brief)**
   - Last commit hash and message
   - Files changed (stat line)
   - If already up-to-date, say "Already up to date" and stop

4. **Non-ACI repositories**
   - External reposities can be cloned as extended knowledgebase inside different folders under `/root/repo/` directory inside the same sandbox and same methodology 

4. **Read files locally**
   - Use `cat`, `head`, `grep` instead of web fetch tools
   - Examples:
     - `cat /root/repo/aci/soul.txt`
     - `head -100 /root/repo/aci/_prime_directive.md`
     - `grep -n "TVA" /root/repo/aci/_tva.md`
     - `ls /root/repo/aci/` to list available files

5. **Only use web fetch when:**
   - The local clone is confirmed outdated or corrupted
   - The file does not exist in the local clone
   - You need a file that was just committed and the pull failed

## Key Rules
- Always prefer local reads (cat, head, grep) over fetch_generic_url_content or read_url for ACI files
- Sync first before reading if the user asks for the latest state
- Keep reports brief: commit hash + message + changed files is enough
- Do not fabricate file contents — read them from disk
- If git pull fails, report the error, do not silently fall back to web fetch