---
description: Start every new session by reading project state — TODO, WORK_DONE, and ISSUE_TRACKER
---

# /start — Agent Session Initialization

This workflow MUST be executed at the beginning of every new AI agent session working on the GreaterWMS project. It ensures the agent has full context before making any changes.

## Steps

// turbo-all

1. **Read the master TODO list** to understand what work is pending, in-progress, and completed:
   ```bash
   cat /Users/venkatakrishnanshankar/Downloads/GreaterWMS-master/TODO.md
   ```

2. **Read the Work Done register** to understand what has already been accomplished:
   ```bash
   cat /Users/venkatakrishnanshankar/Downloads/GreaterWMS-master/WORK_DONE.md
   ```

3. **Read the Issue Tracker** to understand all known issues and their status:
   ```bash
   cat /Users/venkatakrishnanshankar/Downloads/GreaterWMS-master/ISSUE_TRACKER.md
   ```

4. **Summarize the current state** to the user:
   - How many TODO items remain per priority (P0/P1/P2/P3)
   - How many issues are Open vs Resolved
   - What was the last completed work entry
   - Recommend the next task to work on (highest priority open item)

## Rules

- **NEVER skip this workflow** when starting a new session on this project
- After reading, present a brief status summary to the user
- Ask the user which TODO item or issue they want to work on, or suggest the highest-priority open item
- If the user gives a task, cross-reference it with the TODO and ISSUE_TRACKER before starting
- When starting work on any item, mark it as `[/]` in `TODO.md` immediately
