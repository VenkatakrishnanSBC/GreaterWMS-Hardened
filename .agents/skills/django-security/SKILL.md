---
name: django-security
description: Django security hardening — CSRF, authentication, permissions, HTTPS, headers
---

# Django Security Hardening Skill

Use this skill when fixing security issues (ISS-001 through ISS-014) or implementing TODO items SEC-001 through SEC-014.

## Checklist

### 1. CSRF Protection
```python
# settings.py — MIDDLEWARE must include:
'django.middleware.csrf.CsrfViewMiddleware',

# For API endpoints using token auth, exempt them explicitly:
from django.views.decorators.csrf import csrf_exempt
```

### 2. DEBUG & ALLOWED_HOSTS
```python
import os
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

### 3. SECRET_KEY from Environment
```python
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY environment variable is required")
```

### 4. Proper JWT Authentication
```python
# Replace openid-based auth with JWT:
# 1. Generate JWT on login with expiration (e.g., 24 hours)
# 2. Validate JWT on every request (check signature + expiration)
# 3. Implement refresh token mechanism
# 4. Store JWT_SALT in environment variable
```

### 5. RBAC Permission System
```python
# Implement roles: Admin, Manager, Operator, Viewer
# Map permissions to roles:
# - Admin: full CRUD on all resources
# - Manager: CRUD on own tenant resources
# - Operator: read + create/update (no delete)
# - Viewer: read-only
```

### 6. CORS Configuration
```python
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = os.environ.get('CORS_WHITELIST', 'http://localhost:8080').split(',')
```

### 7. HTTPS Enforcement
```python
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 8. Input Validation
```python
# Replace regex-based validation with:
# 1. Django form/serializer validation
# 2. bleach library for HTML sanitization
# 3. Django ORM parameterized queries (already safe from SQLi)
# 4. Remove naive script/select regex checks
```

## Verification
```bash
# Run Django deployment checks:
python manage.py check --deploy

# Run Bandit security scan:
bandit -r . -x ./venv,./migrations -ll
```
