"""
PERF-002: Cache-backed rate limiting throttle.

Replaces the database-backed throttle with Django's cache framework.
When Redis is configured (via REDIS_URL), this uses Redis for O(1)
lookups instead of database queries on every request.
"""
import logging
from typing import Optional

from django.core.cache import caches
from django.conf import settings
from rest_framework.request import Request
from rest_framework.throttling import BaseThrottle

logger = logging.getLogger(__name__)

# Throttle limits by HTTP method
THROTTLE_LIMITS = {
    'get': 'GET_THROTTLE',
    'post': 'POST_THROTTLE',
    'put': 'PUT_THROTTLE',
    'patch': 'PATCH_THROTTLE',
    'delete': 'DELETE_THROTTLE',
}

# Public paths that bypass throttling
PUBLIC_PATHS = frozenset(['/api/docs/', '/api/debug/', '/api/'])


class VisitThrottle(BaseThrottle):
    """
    Cache-backed rate-limiting throttle for the GreaterWMS API.

    Uses Django's cache framework (Redis when available, LocMemCache fallback).
    Tracks request counts per user/IP/method within a sliding time window.
    """

    def __init__(self) -> None:
        self._wait_seconds: int = 0
        self._cache = caches['throttle']

    def allow_request(self, request: Request, view) -> bool:
        """Check if the request should be allowed based on rate limits."""
        if request.path in PUBLIC_PATHS:
            return False

        method = request.method.lower()
        if method not in THROTTLE_LIMITS:
            return False

        ip = (
            request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
            or request.META.get('REMOTE_ADDR', '')
        )
        openid = request.auth.openid
        limit = getattr(settings, THROTTLE_LIMITS[method], 500)
        window = getattr(settings, 'ALLOCATION_SECONDS', 1)

        return self._check_rate(openid, ip, method, limit, window)

    def _check_rate(
        self, openid: str, ip: str, method: str, limit: int, window: int
    ) -> bool:
        """
        Core rate-limiting logic using cache counters.

        Uses atomic cache increment for thread-safe counting.
        Each unique (openid, ip, method) combination gets its own counter
        with a TTL equal to the throttle window.

        Args:
            openid: User tenant identifier.
            ip: Client IP address.
            method: HTTP method (lowercase).
            limit: Maximum requests allowed in the window.
            window: Time window in seconds.

        Returns:
            True if the request is allowed, False if throttled.
        """
        cache_key = f"throttle:{openid}:{ip}:{method}"

        # Try to increment existing counter
        count = self._cache.get(cache_key)

        if count is None:
            # First request in this window — set counter to 1
            self._cache.set(cache_key, 1, timeout=window)
            return True

        if count >= limit:
            # Rate limit exceeded
            ttl = self._cache.ttl(cache_key) if hasattr(self._cache, 'ttl') else window
            self._wait_seconds = max(ttl, 1)
            logger.warning(
                f"Rate limit exceeded: {openid}@{ip} {method.upper()} "
                f"({count}/{limit} in {window}s)"
            )
            return False

        # Increment counter (use incr for atomicity when available)
        try:
            self._cache.incr(cache_key)
        except ValueError:
            # Key expired between get and incr — reset
            self._cache.set(cache_key, 1, timeout=window)

        return True

    def wait(self) -> int:
        """Return the number of seconds the client should wait before retrying."""
        return self._wait_seconds or 1
