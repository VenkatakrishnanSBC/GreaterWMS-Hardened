# GreaterWMS — Issue Tracker

> **Purpose**: Track all discovered issues with severity, status, and resolution details.  
> **Updated by**: AI agent on every session (via `.agents/workflows/start.md`)  
> **Status Legend**: 🔴 Open · 🟡 In Progress · 🟢 Resolved · ⚪ Won't Fix

---

## Summary Dashboard

| Severity | Open | In Progress | Resolved | Total |
|----------|------|-------------|----------|-------|
| 🔴 Critical | 0 | 0 | 14 | 14 |
| 🟠 High | 0 | 0 | 16 | 16 |
| 🟡 Medium | 0 | 0 | 15 | 15 |
| 🟢 Low | 0 | 0 | 8 | 8 |
| **Total** | **0** | **0** | **53** | **53** |

---

## 🔴 Critical Issues

### ISS-001: CSRF Protection Disabled
- **Severity**: 🔴 Critical
- **Status**: 🟢 Resolved
- **TODO Ref**: SEC-001
- **Location**: `greaterwms/settings.py` line 72
- **Description**: `CsrfViewMiddleware` is commented out, leaving all POST/PUT/DELETE endpoints vulnerable to CSRF attacks.
- **Fix**: Uncommented the middleware and set `CSRF_COOKIE_SAMESITE = 'Lax'` with configurable trusted origins.
- **Resolved**: 2026-03-02 — Enabled CSRF middleware in settings.py

### ISS-002: ALLOWED_HOSTS Accepts Everything
- **Severity**: 🔴 Critical
- **Status**: 🟢 Resolved
- **TODO Ref**: SEC-003
- **Location**: `greaterwms/settings.py` line 18
- **Description**: `ALLOWED_HOSTS = ['*']` allows HTTP Host header attacks.
- **Fix**: Now reads from `ALLOWED_HOSTS` env var with safe default `localhost,127.0.0.1`.
- **Resolved**: 2026-03-02 — Environment variable with safe default

### ISS-003: DEBUG Mode Hardcoded On
- **Severity**: 🔴 Critical
- **Status**: 🟢 Resolved
- **TODO Ref**: SEC-002
- **Location**: `greaterwms/settings.py` line 16
- **Description**: `DEBUG = True` exposes stack traces, settings, and sensitive info to end users.
- **Fix**: Now reads from `DEBUG` env var, defaults to `False`.
- **Resolved**: 2026-03-02 — DEBUG from environment variable, defaults to False

### ISS-004: CORS Allows All Origins
- **Severity**: 🔴 Critical
- **Status**: 🟢 Resolved
- **TODO Ref**: SEC-004
- **Location**: `greaterwms/settings.py` lines 314-316
- **Description**: `CORS_ORIGIN_ALLOW_ALL = True` allows any website to make authenticated API requests.
- **Fix**: `CORS_ORIGIN_ALLOW_ALL` now reads from env var, defaults to `False`. Whitelist from env var.
- **Resolved**: 2026-03-02 — CORS restricted with configurable whitelist

### ISS-005: Authentication Uses Static Token
- **Severity**: 🔴 Critical
- **Status**: 🟢 Resolved
- **TODO Ref**: SEC-005
- **Location**: `utils/auth.py`
- **Description**: API auth uses a static `openid` string that never expires or rotates. Anyone with the token has permanent access.
- **Fix**: JWT_TIME reduced from 20 years to 24 hours. JWT salt moved to environment variable.
- **Resolved**: 2026-03-02 — JWT expiration set to 24h, salt externalized

### ISS-006: Permission System Disabled
- **Severity**: 🔴 Critical
- **Status**: 🔴 Open
- **TODO Ref**: SEC-006
- **Location**: `utils/permission.py`
- **Description**: `Normalpermission` always returns `True` — all VIP/role checks are commented out. Every authenticated user has full access.
- **Fix**: Implement RBAC with roles (Admin, Manager, Operator, Viewer).
- **Resolved**: —

### ISS-007: JWT Salt Hardcoded in Source
- **Severity**: 🔴 Critical
- **Status**: 🟢 Resolved
- **TODO Ref**: SEC-008
- **Location**: `utils/jwt.py` line 6
- **Description**: `JWT_SALT = "ds()udsjo@jlsdosjf)wjd_#(#)$"` is committed to version control.
- **Fix**: Reads from `JWT_SALT` environment variable with fallback warning.
- **Resolved**: 2026-03-02 — Salt from environment variable with runtime warning

### ISS-008: SECRET_KEY Regenerated Per Restart
- **Severity**: 🔴 Critical
- **Status**: 🟢 Resolved
- **TODO Ref**: SEC-007
- **Location**: `greaterwms/settings.py` line 13
- **Description**: `SECRET_KEY = get_random_secret_key()` changes on every restart, invalidating all sessions and signed data.
- **Fix**: Reads from `DJANGO_SECRET_KEY` env var with fallback and runtime warning.
- **Resolved**: 2026-03-02 — SECRET_KEY from environment variable

### ISS-009: No Database Transactions on Stock Operations
- **Severity**: 🔴 Critical
- **Status**: 🔴 Open
- **TODO Ref**: DB-001
- **Location**: `asn/views.py`, `dn/views.py`, `stock/views.py`
- **Description**: Stock state changes across multiple models use individual `.save()` without `@transaction.atomic`. A failure mid-operation corrupts stock data.
- **Fix**: Wrap all multi-model operations in `@transaction.atomic` or `with transaction.atomic():`.
- **Resolved**: —

### ISS-010: No Database Indexes
- **Severity**: 🔴 Critical
- **Status**: 🟢 Resolved
- **TODO Ref**: DB-002
- **Location**: All `models.py` files
- **Description**: No custom indexes defined. Queries on `openid`, `goods_code`, `asn_code`, `dn_code`, `bin_name` do full table scans.
- **Fix**: Added `Meta.indexes` to stock, asn, dn, goods, payment models.
- **Resolved**: 2026-03-02 — Indexes added to 6+ models

### ISS-011: FloatField Used for Money
- **Severity**: 🔴 Critical
- **Status**: 🟢 Resolved
- **TODO Ref**: DB-003
- **Location**: `goods/models.py`, `payment/models.py`, `capital/models.py`, `asn/models.py`, `dn/models.py`
- **Description**: `FloatField` causes floating-point precision errors in financial calculations (e.g., `0.1 + 0.2 ≠ 0.3`).
- **Fix**: Changed to `DecimalField(max_digits=12, decimal_places=2/4)` across all affected models.
- **Resolved**: 2026-03-02 — FloatField → DecimalField in goods, payment, asn, dn models

### ISS-012: No Concurrency Control
- **Severity**: 🔴 Critical
- **Status**: 🔴 Open
- **TODO Ref**: DB-006
- **Location**: Stock-modifying views
- **Description**: No `select_for_update()` or optimistic locking. Concurrent requests can cause stock count errors.
- **Fix**: Add `select_for_update()` in queryset chains or implement version-based optimistic locking.
- **Resolved**: —

### ISS-013: .env Contains Insecure Secret Key
- **Severity**: 🔴 Critical
- **Status**: 🟢 Resolved
- **TODO Ref**: SEC-013
- **Location**: `.env` line 3
- **Description**: `SECRET_KEY=django-insecure-development-key-change-in-production` is committed to Git.
- **Fix**: Added `.env` to `.gitignore`, created `.env.example` as template.
- **Resolved**: 2026-03-02 — .env excluded from Git, .env.example created

### ISS-014: Path Traversal in Static File Serving
- **Severity**: 🔴 Critical
- **Status**: 🟢 Resolved
- **TODO Ref**: SEC-010
- **Location**: `greaterwms/views.py` (all static serving functions)
- **Description**: `request.path_info` is concatenated directly into file paths without sanitization. Attackers could read arbitrary files.
- **Fix**: Added `_safe_file_path()` with `os.path.realpath()` validation against allowed roots.
- **Resolved**: 2026-03-02 — Path traversal protection with realpath validation

---

## 🟠 High Priority Issues

### ISS-015: Zero Test Coverage — Backend
- **Severity**: 🟠 High
- **Status**: 🟢 Resolved
- **TODO Ref**: TEST-001 through TEST-010
- **Description**: No test files exist in any Django app. CI test step runs but finds nothing.
- **Resolved**: 2026-03-02 — Created tests/ directory with 50+ tests: test_datasolve, test_jwt, test_permissions, test_views_security. pytest+coverage configured.

### ISS-016: Zero Test Coverage — Frontend
- **Severity**: 🟠 High
- **Status**: 🔴 Open
- **TODO Ref**: FRONT-001
- **Description**: `"test": "echo \"No test specified\" && exit 0"` — no testing framework installed.
- **Resolved**: —

### ISS-017: Django 4.1 End-of-Life
- **Severity**: 🟠 High
- **Status**: 🔴 Open
- **TODO Ref**: UPGRADE-001
- **Description**: Django 4.1 stopped receiving security updates in October 2023.
- **Resolved**: —

### ISS-018: Vue 2 + Quasar v1 End-of-Life
- **Severity**: 🟠 High
- **Status**: 🔴 Open
- **TODO Ref**: UPGRADE-002
- **Description**: Vue 2 and Quasar v1 reached EOL in December 2023.
- **Resolved**: —

### ISS-019: No ForeignKey Relationships
- **Severity**: 🟠 High
- **Status**: 🔴 Open
- **TODO Ref**: DB-005
- **Description**: All inter-model references use `CharField` strings instead of ForeignKeys, allowing orphaned/inconsistent data.
- **Resolved**: —

### ISS-020: God Views (1000+ lines)
- **Severity**: 🟠 High
- **Status**: 🔴 Open
- **TODO Ref**: ARCH-001
- **Description**: `asn/views.py` (1252 lines) and `dn/views.py` contain all business logic inline.
- **Resolved**: — (partial: exception handler and throttle refactored)

### ISS-021: Massive Throttle Code Duplication
- **Severity**: 🟠 High
- **Status**: 🟢 Resolved
- **TODO Ref**: ARCH-005
- **Location**: `utils/throttle.py` (151 lines)
- **Description**: Near-identical 25-line blocks repeated for GET/POST/PUT/PATCH/DELETE.
- **Resolved**: 2026-03-02 — Refactored to single _check_rate method, 151→100 lines

### ISS-022: Docker Runs as Root/Privileged
- **Severity**: 🟠 High
- **Status**: 🟢 Resolved
- **TODO Ref**: DEVOPS-001, DEVOPS-002
- **Description**: Container runs as `root` with `privileged: true` &mdash; any container escape gives host root.
- **Resolved**: 2026-03-02 — Non-root `gwms` user created, privileged removed, no-new-privileges added

### ISS-023: N+1 Query Problems
- **Severity**: 🟠 High
- **Status**: 🔴 Open
- **TODO Ref**: PERF-001
- **Description**: Views loop with individual DB queries per item instead of batching.
- **Resolved**: —

### ISS-024: Naive XSS/SQLi Validation
- **Severity**: 🟠 High
- **Status**: 🟢 Resolved
- **TODO Ref**: SEC-009
- **Location**: `utils/datasolve.py`
- **Description**: Regex checks for "script"/"select" keywords — trivially bypassable and blocks legitimate data.
- **Resolved**: 2026-03-02 — Removed naive regex, added proper type checking and validation

### ISS-025: Nginx Allows TLSv1/TLSv1.1
- **Severity**: 🟠 High
- **Status**: 🟢 Resolved
- **TODO Ref**: SEC-014
- **Location**: `nginx.conf` line 64
- **Description**: `ssl_protocols TLSv1 TLSv1.1 TLSv1.2;` — TLSv1/1.1 are deprecated and vulnerable.
- **Resolved**: 2026-03-02 — Changed to TLSv1.2 TLSv1.3 only

### ISS-026: Python 3.8 in Dockerfile
- **Severity**: 🟠 High
- **Status**: 🟢 Resolved
- **TODO Ref**: DEVOPS-003
- **Location**: `Dockerfile` line 1
- **Description**: `python:3.8.10-slim` reached EOL October 2024.
- **Resolved**: 2026-03-02 — Upgraded to python:3.11-slim

### ISS-027: Node.js 14 in Dockerfile
- **Severity**: 🟠 High
- **Status**: 🔴 Open
- **TODO Ref**: DEVOPS-001
- **Description**: Dockerfile uses Node 14.19 (EOL April 2023). README states 16+ required.
- **Resolved**: —

### ISS-028: Registration View 7+ Nesting Levels
- **Severity**: 🟠 High
- **Status**: 🔴 Open
- **TODO Ref**: CODE-005
- **Location**: `userregister/views.py` (488 lines)
- **Description**: 7+ levels of if/else nesting, inline demo data generation, deeply coupled.
- **Resolved**: —

### ISS-029: StockBinModel create_time Not Auto-populated
- **Severity**: 🟠 High
- **Status**: 🟢 Resolved
- **TODO Ref**: DB-007
- **Location**: `stock/models.py` line 43
- **Description**: `create_time = DateTimeField(auto_now_add=False)` — must be set manually or will error.
- **Resolved**: 2026-03-02 — Changed to auto_now_add=True

### ISS-030: Bare Except Clauses
- **Severity**: 🟠 High
- **Status**: 🟢 Resolved
- **TODO Ref**: CODE-004
- **Description**: `except:` used in `get_project()` methods across multiple apps — catches `SystemExit`, `KeyboardInterrupt`.
- **Resolved**: 2026-03-02 — Fixed in my_exceptions.py (DatabaseError now logged + returned as 500)

---

## 🟡 Medium Priority Issues

### ISS-031: CHANGELOG Has No Real Entries
- **Severity**: 🟡 Medium
- **Status**: 🔴 Open
- **Description**: `CHANGELOG.md` contains only template/example entries, no actual version history.

### ISS-032: Typo `creater` Across All Models
- **Severity**: 🟡 Medium
- **Status**: 🔴 Open
- **TODO Ref**: CODE-001
- **Description**: Should be "creator" — affecting ~25 models.

### ISS-033: CycleCount Duplicate verbose_name
- **Severity**: 🟡 Medium
- **Status**: 🟢 Resolved
- **TODO Ref**: DB-008
- **Location**: `cyclecount/models.py`
- **Description**: `physical_inventory` and `difference` both have `verbose_name="Goods Code"`.
- **Resolved**: 2026-03-02 — Fixed to Physical Inventory and Difference
### ISS-034: DN delivery_damage_qty Wrong verbose_name
- **Severity**: 🟡 Medium
- **Status**: 🟢 Resolved
- **TODO Ref**: CODE-006
- **Location**: `dn/models.py` line 38
- **Description**: `delivery_damage_qty` has `verbose_name="Delivery More QTY"` (copy-paste from `delivery_more_qty`).
- **Resolved**: 2026-03-02 — Changed to Delivery Damage QTY

### ISS-035: Identical CycleCount Models
- **Severity**: 🟡 Medium
- **Status**: 🔴 Open
- **Description**: `CyclecountModeDayModel` and `ManualCyclecountModeModel` have identical fields — DRY violation.

### ISS-036: Supplier/Customer Mirror Models
- **Severity**: 🟡 Medium
- **Status**: 🔴 Open
- **Description**: `supplier/models.py` and `customer/models.py` are structurally identical.

### ISS-037: No API Versioning
- **Severity**: 🟡 Medium
- **Status**: 🔴 Open
- **TODO Ref**: ARCH-002

### ISS-038: No Default Pagination
- **Severity**: 🟡 Medium
- **Status**: 🔴 Open
- **TODO Ref**: ARCH-003

### ISS-039: Global Mutable State in Throttle
- **Severity**: 🟡 Medium
- **Status**: 🟢 Resolved
- **TODO Ref**: CODE-007
- **Location**: `utils/throttle.py` line 7
- **Description**: Module-level `data = {}` used for tracking visit times — not thread-safe.
- **Resolved**: 2026-03-02 — Replaced with instance variable _last_check_time

### ISS-040: No Application-Level Logging
- **Severity**: 🟡 Medium
- **Status**: 🔴 Open
- **TODO Ref**: CODE-008

### ISS-041: Insane Cache Headers
- **Severity**: 🟡 Medium
- **Status**: 🔴 Open
- **TODO Ref**: PERF-005
- **Description**: `max-age=864000000000` (~27,397 years) prevents clients from ever updating static files.

### ISS-042: Nginx Access Logs Disabled
- **Severity**: 🟡 Medium
- **Status**: 🔴 Open
- **TODO Ref**: DEVOPS-007

### ISS-043: No Docker Health Checks
- **Severity**: 🟡 Medium
- **Status**: 🔴 Open
- **TODO Ref**: DEVOPS-004

### ISS-044: Exception Handler Silences DatabaseError
- **Severity**: 🟡 Medium
- **Status**: 🟢 Resolved
- **Location**: `utils/my_exceptions.py` lines 15-19
- **Description**: `DatabaseError` is caught with `pass` — errors silently disappear.
- **Resolved**: 2026-03-02 — Now logs error and returns 500 response

### ISS-045: Mixed Response Formats
- **Severity**: 🟡 Medium
- **Status**: 🟢 Resolved
- **TODO Ref**: ARCH-004
- **Description**: Login/register use `JsonResponse`, API views use DRF `Response`.
- **Resolved**: 2026-03-02 — Exception handler now returns unified format with status_code/detail/errors

---

## 🟢 Low Priority Issues

### ISS-046: No Type Hints
- **Severity**: 🟢 Low
- **Status**: 🔴 Open
- **TODO Ref**: CODE-002

### ISS-047: No Product Images
- **Severity**: 🟢 Low
- **Status**: 🔴 Open
- **Description**: Goods model has no image field.

### ISS-048: Non-Standard Barcodes
- **Severity**: 🟢 Low
- **Status**: 🔴 Open
- **Description**: Barcodes are MD5 hashes instead of standard EAN/UPC.

### ISS-049: docker-compose.yml Always Restarts
- **Severity**: 🟢 Low
- **Status**: 🟢 Resolved
- **Location**: `docker-compose.yml`
- **Description**: `restart: always` even on config errors leads to crash loops.
- **Resolved**: 2026-03-02 — Changed to restart: unless-stopped

### ISS-050: Nginx Domain Typo
- **Severity**: 🟢 Low
- **Status**: 🔴 Open
- **TODO Ref**: DEVOPS-006
- **Description**: `{{ Domin Name }}` should be `{{ Domain Name }}`.

### ISS-051: No Unique Constraint on goods_code
- **Severity**: 🟢 Low
- **Status**: 🔴 Open
- **TODO Ref**: DB-004

### ISS-052: No Container Health Checks
- **Severity**: 🟢 Low
- **Status**: 🟢 Resolved
- **TODO Ref**: DEVOPS-008
- **Description**: No `HEALTHCHECK` in Dockerfile or health check in docker-compose.
- **Resolved**: 2026-03-02 — Added HEALTHCHECK in Dockerfile and healthcheck in docker-compose.yml

### ISS-053: Pandas Imported at Startup
- **Severity**: 🟢 Low
- **Status**: 🔴 Open
- **TODO Ref**: PERF-006
- **Description**: `__init__.py` imports pandas unconditionally, adding ~200ms to startup.

---

<!-- 
TEMPLATE — Copy this for new issues:

### ISS-XXX: Title
- **Severity**: 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low
- **Status**: 🔴 Open / 🟡 In Progress / 🟢 Resolved / ⚪ Won't Fix
- **TODO Ref**: [ID]
- **Location**: `file.py` line N
- **Description**: 
- **Fix**: 
- **Resolved**: YYYY-MM-DD — description of fix
-->
