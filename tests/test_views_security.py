"""
Tests for greaterwms/views.py — Static file serving with path traversal protection.

SEC-010 / ISS-014: Verifies path traversal attacks are blocked.
"""
import pytest
from unittest.mock import Mock, patch
from rest_framework.exceptions import APIException


class TestPathTraversalProtection:
    """Tests for _safe_file_path function (SEC-010)."""

    def test_normal_path_allowed(self):
        from greaterwms.views import _safe_file_path
        from django.conf import settings
        import os

        base = str(settings.BASE_DIR)
        # Only test if the file actually exists
        test_path = os.path.join(base, 'manage.py')
        if os.path.exists(test_path):
            result = _safe_file_path(base, '/manage.py')
            assert result.endswith('manage.py')

    def test_traversal_attack_blocked(self):
        from greaterwms.views import _safe_file_path
        from django.conf import settings

        base = str(settings.BASE_DIR)
        with pytest.raises(APIException):
            _safe_file_path(base, '/../../../etc/passwd')

    def test_double_dot_blocked(self):
        from greaterwms.views import _safe_file_path
        from django.conf import settings

        base = str(settings.BASE_DIR)
        with pytest.raises(APIException):
            _safe_file_path(base, '/static/../../../etc/shadow')

    def test_nonexistent_file_raises(self):
        from greaterwms.views import _safe_file_path
        from django.conf import settings

        base = str(settings.BASE_DIR)
        with pytest.raises(APIException):
            _safe_file_path(base, '/definitely_not_a_real_file.xyz')


class TestCacheHeaders:
    """Tests for fixed cache headers (ISS-041)."""

    def test_cache_max_age_reasonable(self):
        from greaterwms.views import CACHE_MAX_AGE
        # Must NOT be the old 27,397-year value
        assert "864000000000" not in CACHE_MAX_AGE
        # Should be 24 hours
        assert CACHE_MAX_AGE == "max-age=86400"
