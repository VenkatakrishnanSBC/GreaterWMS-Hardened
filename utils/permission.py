import logging
from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)


# SEC-006 / ISS-006: Basic RBAC permission system
# Replaces the always-True permission class with role-based checks.
# Roles are defined by the user's `staff_type` or similar field.
# For now, we implement a proper base with future role extension points.

class Normalpermission(BasePermission):
    """
    Base permission class for GreaterWMS API.

    Currently allows all authenticated users (maintaining backward compatibility),
    but provides the structure for role-based access control.

    To restrict a view to specific roles, override `allowed_roles` in the view:

        class MyViewSet(viewsets.ModelViewSet):
            permission_classes = [Normalpermission]
            allowed_roles = ['admin', 'manager']
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        Checks:
        1. User must be authenticated (request.auth is not None)
        2. If the view defines `allowed_roles`, user's role must match
        """
        # Must be authenticated
        if not request.auth or request.auth is False:
            return False

        # Check role-based access if the view defines allowed_roles
        allowed_roles = getattr(view, 'allowed_roles', None)
        if allowed_roles is not None:
            user_role = getattr(request.auth, 'staff_type', None)
            if user_role not in allowed_roles:
                logger.warning(
                    f"Permission denied: user role '{user_role}' "
                    f"not in allowed roles {allowed_roles} for {view.__class__.__name__}"
                )
                return False

        return True

    def has_object_permission(self, request, view, obj=None):
        """
        Object-level permission check.

        Ensures users can only access objects belonging to their tenant (openid).
        """
        if not request.auth or request.auth is False:
            return False

        # Multi-tenancy: users can only access their own data
        if hasattr(obj, 'openid') and hasattr(request.auth, 'openid'):
            if obj.openid != request.auth.openid:
                logger.warning(
                    f"Tenant isolation violation: user {request.auth.openid} "
                    f"attempted to access object owned by {obj.openid}"
                )
                return False

        return True
