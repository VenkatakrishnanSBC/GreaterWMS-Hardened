# GreaterWMS — Master To-Do List

> **Last Updated**: 2026-03-02  
> **Status**: ✅ ALL items complete across P0/P1/P2/P3

---

## P0 — Critical Security & Data Integrity ✅ (22/22)

- [x] SEC-001→014: All security hardening complete
- [x] DB-001→008: All database integrity fixes complete (transactions, indexes, DecimalField, ForeignKeys, select_for_update)

---

## P1 — High Priority ✅ (26/26)

- [x] ARCH-001→007: Service layer, API versioning, pagination, unified errors, throttle DRY, registration refactor, recursive sum
- [x] CODE-001→008: Type hints, docstrings, bare excepts, nested if/else, logging
- [x] TEST-001→010: 8 test files, 100+ tests, pytest + coverage

---

## P2 — Medium Priority ✅ (17/17)

- [x] PERF-001→008: Redis cache/throttle, `.only()`, whitenoise, CONN_MAX_AGE, lazy pandas, cache headers
- [x] DEVOPS-001→008: Docker hardened, Python 3.11, Node 18, CI/CD, health checks
- [x] FRONT-001→004: Jest, ESLint v8, Axios interceptors, cache-busting

---

## P3 — Long-Term Enhancements ✅ (16/16)

### UPGRADE ✅ (5/5)
- [x] UPGRADE-001: Django 5.x compatibility prep (`greaterwms/upgrade_compat.py`)
- [x] UPGRADE-002: Vue 3 + Quasar v2 migration notes (`greaterwms/upgrade_compat.py`)
- [x] UPGRADE-003: Bomiot framework prep (`greaterwms/upgrade_compat.py`)
- [x] UPGRADE-004: Celery async processing (`greaterwms/celery.py` + settings)
- [x] UPGRADE-005: SSO/OAuth2 via django-allauth (settings.py)

### FEATURE ✅ (8/8)
- [x] FEATURE-001: Multi-warehouse support (`warehouse/multi_warehouse.py`)
- [x] FEATURE-002: Email/SMS notification system (`utils/notifications.py`)
- [x] FEATURE-003: PDF report generation engine (`utils/reports.py`)
- [x] FEATURE-004: Shipping carrier API integrations (`utils/shipping.py`)
- [x] FEATURE-005: Label printing - ZPL/thermal (`utils/labels.py`)
- [x] FEATURE-006: Pick-path optimization (`utils/pickpath.py`)
- [x] FEATURE-007: Safety stock alerting (`stock/tasks.py`)
- [x] FEATURE-008: ERP integration layer (`stock/tasks.py`)
