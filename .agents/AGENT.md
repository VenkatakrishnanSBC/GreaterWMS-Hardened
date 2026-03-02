---
name: GreaterWMS Agent System
description: Master agent configuration defining all personas, skills, and workflows for the GreaterWMS project
---

# GreaterWMS — Agent System Configuration

This document defines the complete agent ecosystem for the GreaterWMS project. It connects **personas** (domain experts), **skills** (technical capabilities), and **workflows** (structured processes) into a unified system.

---

## How This System Works

```
┌─────────────────────────────────────────────────────┐
│                  /start Workflow                     │
│   Reads: TODO.md → WORK_DONE.md → ISSUE_TRACKER.md │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              /discuss Workflow                        │
│   Invokes relevant personas for requirement inputs   │
│                                                      │
│   👷 Warehouse Mgr  │  📦 Inbound Mgr               │
│   🚚 Outbound Mgr   │  🔒 Compliance Mgr            │
│   📊 Export Mgr      │  📝 Doc Specialist             │
│   💻 Dev Lead        │  🧪 QA Lead                    │
│   🏗️ DevOps Lead     │  🎨 UX Lead                    │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              /fix-issue Workflow                      │
│   Uses Skills: Security, DB, API, Testing, etc.      │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│           /update-tracker Workflow                    │
│   Syncs: TODO.md ← WORK_DONE.md ← ISSUE_TRACKER.md │
└─────────────────────────────────────────────────────┘
```

## Persona Roster

| Persona | ID | Expertise | Consulted For |
|---------|----|-----------|--------------| 
| Warehouse Manager | `@warehouse-mgr` | Operations, layout, bin strategy | Stock, bin, cycle count, warehouse config |
| Inbound Manager | `@inbound-mgr` | Receiving, ASN, put-away | ASN module, supplier integration, quality check |
| Outbound Manager | `@outbound-mgr` | Picking, packing, shipping | DN module, picking strategy, driver dispatch |
| Compliance & Security Manager | `@compliance-mgr` | Security, audit, regulations | Auth, permissions, data protection, audit trails |
| Export & Reporting Manager | `@export-mgr` | Reports, analytics, data export | Dashboard, Excel/CSV export, KPIs |
| Documentation Specialist | `@doc-specialist` | API docs, user guides, changelogs | README, API docs, CHANGELOG, inline docs |
| Development Lead | `@dev-lead` | Architecture, code quality, patterns | Refactoring, service layer, design patterns |
| QA & Testing Lead | `@qa-lead` | Testing strategy, quality gates | Test framework, coverage, CI validation |
| DevOps Lead | `@devops-lead` | Docker, CI/CD, deployment, infra | Dockerfile, nginx, GitHub Actions, monitoring |
| UX/Frontend Lead | `@ux-lead` | UI design, frontend architecture | Vue/Quasar components, responsiveness, i18n |

## Skills Available

| Skill | File | Purpose |
|-------|------|---------|
| Django Security | `.agents/skills/django-security/SKILL.md` | CSRF, auth, permissions, HTTPS hardening |
| Database Optimization | `.agents/skills/database-optimization/SKILL.md` | Indexes, transactions, ForeignKeys, DecimalField |
| API Refactoring | `.agents/skills/api-refactoring/SKILL.md` | Service layer, versioning, pagination, response format |
| Testing Strategy | `.agents/skills/testing-strategy/SKILL.md` | pytest setup, fixtures, mocks, coverage targets |
| DevOps Hardening | `.agents/skills/devops-hardening/SKILL.md` | Docker non-root, TLS, health checks, secrets |
| Frontend Modernization | `.agents/skills/frontend-modernization/SKILL.md` | Vue 3, Quasar v2, testing, Axios interceptors |

## Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `/start` | Session begin | Read project state, summarize, recommend next task |
| `/discuss` | Before major features | Gather requirements from relevant personas |
| `/fix-issue` | Issue resolution | Structured read → plan → fix → verify → update |
| `/update-tracker` | After any work | Sync TODO, WORK_DONE, ISSUE_TRACKER |
