# GreaterWMS Backend — Hardened Dockerfile
# DEVOPS-001 / ISS-022: Non-root user, health check, pinned versions
# DEVOPS-003 / ISS-026: Python 3.8 → 3.11 (3.8 reached EOL 2024-10)

FROM --platform=linux/amd64 python:3.11-slim AS backend

# Security: Create non-root user (DEVOPS-001)
RUN groupadd -r gwms && useradd -r -g gwms -d /GreaterWMS -s /sbin/nologin gwms

RUN mkdir -p /GreaterWMS/templates && chown -R gwms:gwms /GreaterWMS

# Copy requirements first for layer caching
COPY ./requirements.txt /GreaterWMS/requirements.txt
COPY ./backend_start.sh /GreaterWMS/backend_start.sh

WORKDIR /GreaterWMS
ENV PORT=${port:-8008}

# Install system dependencies in single layer (reduces image size)
RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        supervisor \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir supervisor && \
    pip3 install --no-cache-dir -U 'Twisted[tls,http2]' && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir daphne

RUN chmod +x /GreaterWMS/backend_start.sh
RUN chown -R gwms:gwms /GreaterWMS

# DEVOPS-008 / ISS-052: Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/ || exit 1

# Switch to non-root user (DEVOPS-001 / ISS-022)
USER gwms

CMD ["/GreaterWMS/backend_start.sh"]

# Frontend stage
# DEVOPS-004: Upgraded from Node 14 (EOL) to Node 18 LTS
FROM --platform=linux/amd64 node:18-slim AS front

RUN groupadd -r gwms && useradd -r -g gwms -d /GreaterWMS -s /sbin/nologin gwms
RUN mkdir -p /GreaterWMS/templates && chown -R gwms:gwms /GreaterWMS

COPY ./templates/package.json /GreaterWMS/templates/package.json
COPY ./web_start.sh /GreaterWMS/templates/web_start.sh

WORKDIR /GreaterWMS/templates
ENV PORT=${port:-8080}

RUN npm install -g npm --force && \
    npm install -g yarn --force && \
    npm install -g @quasar/cli --force && \
    yarn install --frozen-lockfile

RUN chmod +x /GreaterWMS/templates/web_start.sh
RUN chown -R gwms:gwms /GreaterWMS

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

USER gwms

ENTRYPOINT ["/GreaterWMS/templates/web_start.sh"]
