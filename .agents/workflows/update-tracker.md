---
description: Update TODO, WORK_DONE, and ISSUE_TRACKER after completing any task
---

# /update-tracker — Post-Task Tracking Update

This workflow MUST be executed after completing any task or fixing any issue in the GreaterWMS project. It keeps all three tracking documents in sync.

## Steps

1. **Update `TODO.md`**:
   - Mark the completed item as `[x]`
   - If work is partially done, mark as `[/]` (in progress)
   - If new TODO items were discovered during work, add them to the appropriate priority section

2. **Add entry to `WORK_DONE.md`**:
   - Add a new entry at the top of the "Completed Work" section (reverse chronological)
   - Use this exact format:
     ```markdown
     ### YYYY-MM-DD — TODO-ID: Short Title
     - **Status**: ✅ Complete
     - **TODO Ref**: [ID from TODO.md]
     - **Issue Ref**: [ID from ISSUE_TRACKER.md, if applicable]
     - **Files Changed**:
       - `path/to/file.py` — description of change
     - **Testing**: How was this verified?
     - **Notes**: Any additional context
     ```

3. **Update `ISSUE_TRACKER.md`**:
   - If an issue was resolved, change its status from `🔴 Open` to `🟢 Resolved`
   - Add the resolution date and description in the `**Resolved**` field
   - Update the **Summary Dashboard** table counts
   - If new issues were discovered, add them at the end of the appropriate severity section using the next available `ISS-XXX` number

4. **Verify consistency**:
   - Every `[x]` in TODO should have a WORK_DONE entry
   - Every resolved issue in ISSUE_TRACKER should reference the fix
   - TODO IDs and Issue IDs should cross-reference correctly

## Rules

- **NEVER skip this workflow** after completing work
- Be precise about files changed and lines modified
- Include how the fix was tested/verified
- Update the dashboard summary counts in ISSUE_TRACKER.md
- If you discovered new issues during work, log them immediately
