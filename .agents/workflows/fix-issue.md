---
description: Structured workflow for fixing an issue from the ISSUE_TRACKER
---

# /fix-issue — Issue Resolution Workflow

Use this workflow when working on any issue from `ISSUE_TRACKER.md`. It ensures consistent quality across all fixes.

## Steps

1. **Read the issue details** from `ISSUE_TRACKER.md`:
   - Note the `ISS-XXX` number, severity, location, and description
   - Note the linked `TODO Ref` ID
   - Read the suggested fix if provided

2. **Read the affected files**:
   - Open and understand the code at the specified location
   - Identify all related files that may need changes
   - Check if other issues affect the same files (batch fixes when possible)

3. **Plan the fix**:
   - Describe what changes are needed
   - Identify potential side effects
   - Check if database migrations are required

4. **Implement the fix**:
   - Make the code changes
   - Follow existing code style and conventions
   - Add comments where the fix is non-obvious

5. **Verify the fix**:
   - If tests exist, run them: `python manage.py test`
   - If modifying models, verify migrations: `python manage.py makemigrations --check --dry-run`
   - If modifying settings, run system check: `python manage.py check --deploy`
   - Manual verification as appropriate

6. **Update trackers** (execute `/update-tracker`):
   - Mark issue as `🟢 Resolved` in `ISSUE_TRACKER.md`
   - Mark TODO item as `[x]` in `TODO.md`
   - Add work entry in `WORK_DONE.md`

## Rules

- **One issue at a time** unless issues are directly related and share the same files
- Always verify the fix before marking as resolved
- If the fix introduces new issues, log them immediately in `ISSUE_TRACKER.md`
- If a fix requires a database migration, note this clearly in the WORK_DONE entry
- If a fix is too complex or risky, mark the issue as `🟡 In Progress` and discuss with the user
