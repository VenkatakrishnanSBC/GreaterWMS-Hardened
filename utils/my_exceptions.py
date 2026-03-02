import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.db import DatabaseError

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Unified exception handler for the GreaterWMS API.

    ARCH-004 / ISS-045: Ensures consistent response format across all errors.
    ISS-044: No longer silently swallows DatabaseError — logs and returns proper response.
    CODE-004 / ISS-030: Specific exception handling instead of bare except/pass.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Standardize error response format
        response.data = {
            'status_code': response.status_code,
            'detail': response.data.get('detail', str(response.data)),
            'errors': response.data if isinstance(response.data, dict) else None,
        }
        return response

    # Handle unhandled exceptions (ISS-044: no more silent swallowing)
    if isinstance(exc, DatabaseError):
        logger.error(f"Database error: {exc}", exc_info=True)
        return Response(
            {
                'status_code': 500,
                'detail': 'A database error occurred. Please try again.',
                'errors': None,
            },
            status=500
        )

    # Log unexpected errors
    view = context.get('view', None)
    view_name = view.__class__.__name__ if view else 'Unknown'
    logger.error(
        f"Unhandled exception in {view_name}: {exc}",
        exc_info=True
    )
    return Response(
        {
            'status_code': 500,
            'detail': 'An unexpected error occurred. Please try again.',
            'errors': None,
        },
        status=500
    )
