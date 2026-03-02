---
description: Invoke domain-expert personas for collaborative requirement gathering and design discussions
---

# /discuss — Persona-Based Discussion Workflow

Use this workflow before implementing any major feature or change. It simulates a cross-functional meeting by consulting the relevant domain-expert personas for requirements and concerns.

## When to Use
- **Before every P0 or P1 task** in `TODO.md`
- Before major architecture changes
- When the user requests input on a feature
- When multiple modules are affected by a change

## How It Works

1. **Identify the topic** — What feature, fix, or change is being discussed?

2. **Select relevant personas** — Read persona files from `.agents/personas/` based on the modules involved:

   | Module(s) Affected | Personas to Consult |
   |--------------------|---------------------|
   | `stock/`, `binset/`, `cyclecount/` | `@warehouse-mgr`, `@dev-lead` |
   | `asn/`, `supplier/`, `payment/` | `@inbound-mgr`, `@dev-lead` |
   | `dn/`, `customer/`, `driver/` | `@outbound-mgr`, `@dev-lead` |
   | `utils/auth.py`, `utils/permission.py`, security | `@compliance-mgr`, `@dev-lead` |
   | `dashboard/`, Excel/CSV, reports | `@export-mgr`, `@dev-lead` |
   | Documentation, API docs, README | `@doc-specialist` |
   | Test files, CI test steps | `@qa-lead`, `@dev-lead` |
   | Docker, nginx, CI/CD, deployment | `@devops-lead` |
   | `templates/`, frontend components | `@ux-lead`, `@dev-lead` |
   | Architecture-wide changes | **All personas** |

3. **Read the persona files** for each selected persona:
   ```bash
   cat .agents/personas/warehouse-mgr.md
   cat .agents/personas/dev-lead.md
   # etc.
   ```

4. **Conduct the discussion** — For each persona, present their input in this format:

   > **@warehouse-mgr** 👷: *"From an operations standpoint, this change needs to ensure stock accuracy is maintained. We can't afford to have stock records going negative. I need an audit trail showing who changed what and when."*
   >
   > **@dev-lead** 💻: *"Architecturally, I'd recommend wrapping this in `@transaction.atomic` and using `select_for_update()`. We should also add a `StockMovement` ledger model for the audit trail the warehouse team needs."*
   >
   > **@qa-lead** 🧪: *"Before we implement this, we need unit tests for the current stock state machine. Any change without tests is flying blind."*
   >
   > **@compliance-mgr** 🔒: *"The audit trail isn't optional — it's a compliance requirement. Every stock adjustment needs user ID, timestamp, reason code, and before/after values."*

5. **Synthesize requirements** — Combine all persona inputs into a consolidated requirements list:

   ```
   Requirements from discussion:
   ✅ Must use @transaction.atomic for stock changes
   ✅ Must add StockMovement ledger for audit trail
   ✅ Must include user ID, timestamp, reason in ledger
   ✅ Must add unit tests before making changes
   ✅ Must validate stock cannot go negative
   ```

6. **Present to user** — Show the discussion summary and ask for approval before implementing.

## Rules

- **Always read the persona files** before generating their input — don't invent concerns the persona file doesn't mention
- Each persona speaks **in character** using their documented input style
- Personas may **disagree** — present the tradeoffs honestly
- The `@dev-lead` is always included for technical feasibility assessment
- After discussion, create or update the implementation plan before coding
- If a persona raises a blocker, flag it to the user before proceeding
- Keep discussions focused — 3-5 personas per topic, not all 10 every time

## Example Invocation

User says: *"Let's work on fixing the stock transaction safety issue (ISS-009)"*

Agent should:
1. Read `TODO.md` → find `DB-001: Wrap all stock operations in @transaction.atomic`
2. Read `ISSUE_TRACKER.md` → find `ISS-009` details
3. Identify modules: `stock/`, `asn/`, `dn/`
4. Select personas: `@warehouse-mgr`, `@inbound-mgr`, `@outbound-mgr`, `@dev-lead`, `@qa-lead`
5. Read their persona files
6. Generate discussion with each persona's input
7. Synthesize requirements
8. Present to user for approval
9. On approval, proceed with `/fix-issue` workflow
