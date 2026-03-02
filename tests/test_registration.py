"""
Tests for user registration and authentication flow.

TEST-007: Integration tests for user registration flow.
TEST-008: Integration tests for login → authenticated API call.
"""
import pytest
from unittest.mock import Mock, patch
import json


class TestRegistrationValidation:
    """Tests for registration input validation (CODE-005)."""

    def test_register_rejects_empty_password1(self):
        """Registration should reject empty password1."""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.post(
            '/register/',
            data=json.dumps({
                'name': 'testuser',
                'password1': '',
                'password2': 'password123'
            }),
            content_type='application/json'
        )
        from userregister.views import register
        response = register(request)
        data = json.loads(response.content)
        assert response.status_code == 200
        assert data.get('status') != 200  # Should not succeed

    def test_register_rejects_mismatched_passwords(self):
        """Registration should reject non-matching passwords."""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.post(
            '/register/',
            data=json.dumps({
                'name': 'testuser',
                'password1': 'password123',
                'password2': 'different456'
            }),
            content_type='application/json'
        )
        from userregister.views import register
        response = register(request)
        data = json.loads(response.content)
        assert response.status_code == 200
        assert data.get('status') != 200


class TestAuthenticationFlow:
    """Tests for authentication via token header."""

    def test_auth_requires_token_header(self):
        """API requests without TOKEN header should fail."""
        from utils.auth import Authtication
        from rest_framework.exceptions import APIException
        auth = Authtication()
        request = Mock()
        request.path = '/api/goods/'
        request.META = {}

        with pytest.raises(APIException):
            auth.authenticate(request)

    def test_auth_rejects_invalid_token(self):
        """API requests with invalid token should fail."""
        from utils.auth import Authtication
        from rest_framework.exceptions import APIException
        auth = Authtication()
        request = Mock()
        request.path = '/api/goods/'
        request.META = {'HTTP_TOKEN': 'nonexistent-token-value'}

        with pytest.raises(APIException):
            auth.authenticate(request)

    def test_auth_skips_docs_paths(self):
        """API docs paths should bypass authentication."""
        from utils.auth import Authtication
        auth = Authtication()
        request = Mock()
        request.path = '/api/docs/'
        request.META = {}

        result = auth.authenticate(request)
        assert result == (False, None)


class TestSettingsConfiguration:
    """Tests verifying security settings are properly configured."""

    def test_csrf_middleware_enabled(self):
        """SEC-001: CSRF middleware should be enabled."""
        from django.conf import settings
        assert 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE

    def test_pagination_enabled(self):
        """ARCH-003: Default pagination should be configured."""
        from django.conf import settings
        rf = settings.REST_FRAMEWORK
        assert rf.get('DEFAULT_PAGINATION_CLASS') is not None
        assert rf.get('PAGE_SIZE', 0) > 0

    def test_versioning_enabled(self):
        """ARCH-002: API versioning should be configured."""
        from django.conf import settings
        rf = settings.REST_FRAMEWORK
        assert rf.get('DEFAULT_VERSIONING_CLASS') is not None

    def test_logging_configured(self):
        """CODE-008: Django LOGGING should be configured."""
        from django.conf import settings
        assert hasattr(settings, 'LOGGING')
        assert 'handlers' in settings.LOGGING
        assert 'loggers' in settings.LOGGING

    def test_request_size_limits(self):
        """SEC-012: Request size limits should be set."""
        from django.conf import settings
        assert settings.DATA_UPLOAD_MAX_MEMORY_SIZE <= 10 * 1024 * 1024

    def test_jwt_expiration_reasonable(self):
        """SEC-005: JWT should not be valid for 20 years."""
        from django.conf import settings
        assert settings.JWT_TIME <= 86400 * 7  # Max 7 days
