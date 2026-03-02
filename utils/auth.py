"""Authentication backend for GreaterWMS API requests."""
from typing import Optional, Tuple, Union

from rest_framework.exceptions import APIException
from rest_framework.request import Request

from userprofile.models import Users


# Paths that bypass authentication
PUBLIC_PATHS = frozenset(['/api/docs/', '/api/debug/', '/api/'])


class Authtication:
    """
    Token-based authentication for the GreaterWMS API.

    Clients must include the user's ``openid`` token in the ``TOKEN``
    HTTP header. Requests to documentation paths bypass authentication.
    """

    def authenticate(self, request: Request) -> Tuple[bool, Optional[Users]]:
        """
        Authenticate the incoming request.

        Args:
            request: The DRF request object.

        Returns:
            Tuple of (is_authenticated, user_object).

        Raises:
            APIException: If token is missing or invalid.
        """
        if request.path in PUBLIC_PATHS:
            return (False, None)

        token: Optional[str] = request.META.get('HTTP_TOKEN')
        if not token:
            raise APIException({"detail": "Please Add Token To Your Request Headers"})

        # PERF-001: Use .only() to avoid loading unnecessary fields
        user = Users.objects.filter(openid__exact=str(token)).only(
            'id', 'openid', 'appid', 'name', 'developer'
        ).first()
        if user is None:
            raise APIException({"detail": "User Does Not Exists"})
        return (True, user)

    def authenticate_header(self, request: Request) -> Optional[str]:
        """Return the WWW-Authenticate header value (unused for token auth)."""
        return None
