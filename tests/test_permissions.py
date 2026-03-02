"""
Tests for utils/permission.py — RBAC permission system.

SEC-006 / ISS-006: Verifies the new permission system works correctly.
"""
import pytest
from unittest.mock import Mock, MagicMock


class TestNormalpermission:
    """Tests for the Normalpermission class."""

    def _make_request(self, openid="test-user", staff_type=None):
        """Create a mock request with auth."""
        request = Mock()
        request.auth = Mock()
        request.auth.openid = openid
        request.auth.staff_type = staff_type
        return request

    def _make_view(self, allowed_roles=None):
        """Create a mock view with optional allowed_roles."""
        view = Mock()
        if allowed_roles is not None:
            view.allowed_roles = allowed_roles
        else:
            # No allowed_roles attribute — delete if mock auto-creates
            del view.allowed_roles
        return view

    def test_authenticated_user_allowed(self):
        from utils.permission import Normalpermission
        perm = Normalpermission()
        request = self._make_request()
        view = self._make_view()
        assert perm.has_permission(request, view) is True

    def test_unauthenticated_request_denied(self):
        from utils.permission import Normalpermission
        perm = Normalpermission()
        request = Mock()
        request.auth = None
        view = self._make_view()
        assert perm.has_permission(request, view) is False

    def test_false_auth_denied(self):
        from utils.permission import Normalpermission
        perm = Normalpermission()
        request = Mock()
        request.auth = False
        view = self._make_view()
        assert perm.has_permission(request, view) is False

    def test_role_based_access_allowed(self):
        from utils.permission import Normalpermission
        perm = Normalpermission()
        request = self._make_request(staff_type="admin")
        view = self._make_view(allowed_roles=["admin", "manager"])
        assert perm.has_permission(request, view) is True

    def test_role_based_access_denied(self):
        from utils.permission import Normalpermission
        perm = Normalpermission()
        request = self._make_request(staff_type="viewer")
        view = self._make_view(allowed_roles=["admin", "manager"])
        assert perm.has_permission(request, view) is False


class TestObjectPermission:
    """Tests for object-level (tenant isolation) permission."""

    def test_same_tenant_allowed(self):
        from utils.permission import Normalpermission
        perm = Normalpermission()
        request = Mock()
        request.auth = Mock()
        request.auth.openid = "tenant-A"
        obj = Mock()
        obj.openid = "tenant-A"
        assert perm.has_object_permission(request, Mock(), obj) is True

    def test_different_tenant_denied(self):
        from utils.permission import Normalpermission
        perm = Normalpermission()
        request = Mock()
        request.auth = Mock()
        request.auth.openid = "tenant-A"
        obj = Mock()
        obj.openid = "tenant-B"
        assert perm.has_object_permission(request, Mock(), obj) is False

    def test_unauthenticated_object_access_denied(self):
        from utils.permission import Normalpermission
        perm = Normalpermission()
        request = Mock()
        request.auth = None
        assert perm.has_object_permission(request, Mock(), Mock()) is False
