---
name: devops-hardening
description: Docker security, CI/CD improvements, nginx TLS, process management, health checks
---

# DevOps Hardening Skill

Use this skill when implementing TODO items DEVOPS-001 through DEVOPS-008 or fixing issues ISS-022, ISS-025, ISS-026, ISS-027, ISS-042, ISS-043.

## 1. Non-Root Docker

```dockerfile
# Dockerfile — run as non-root user
FROM python:3.11-slim AS backend

RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 8008
CMD ["daphne", "-b", "0.0.0.0", "-p", "8008", "greaterwms.asgi:application"]
```

## 2. Docker Compose Hardening

```yaml
# docker-compose.yml
services:
  backend:
    build:
      context: .
      target: backend
    # REMOVE: privileged: true
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8008/"]
      interval: 30s
      timeout: 10s
      retries: 3
    environment:
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DEBUG=False
```

## 3. Nginx TLS Hardening

```nginx
# nginx.conf — modern TLS only
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;

# Run as non-root:
user www-data;

# Enable access logging:
access_log /var/log/nginx/access.log combined;

# Add security headers:
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'" always;
```

## 4. Supervisord Non-Root

```ini
[program:greaterwms]
directory=/app
user=appuser
command=daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application
```

## 5. Environment Template

```bash
# .env.example (commit this, NOT .env)
DJANGO_SECRET_KEY=change-me-to-a-random-50-char-string
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_WHITELIST=https://yourdomain.com
DATABASE_URL=postgres://user:password@localhost:5432/greaterwms
JWT_SALT=change-me-to-a-random-string
```

## 6. Version Updates

| Component | Current | Target |
|-----------|---------|--------|
| Python | 3.8.10 | 3.11+ |
| Node.js | 14.19 | 20 LTS |
| Django | 4.1.2 | 5.1+ |

## Verification
```bash
# Test Docker build:
docker build -t greaterwms-test .

# Verify non-root:
docker run greaterwms-test whoami  # Should NOT be root

# Test health check:
docker compose up -d
docker compose ps  # Check health status

# SSL test:
openssl s_client -connect yourdomain:443 -tls1  # Should FAIL
openssl s_client -connect yourdomain:443 -tls1_2  # Should SUCCEED
```
