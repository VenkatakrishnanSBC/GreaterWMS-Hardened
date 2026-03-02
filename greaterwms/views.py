from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from wsgiref.util import FileWrapper
from rest_framework.exceptions import APIException
import mimetypes, os
import logging

logger = logging.getLogger(__name__)

# SECURITY: Allowed base directories for static file serving (SEC-010 / ISS-014)
ALLOWED_STATIC_ROOTS = None  # Lazily initialized


def _get_allowed_roots():
    """Get allowed root directories for static file serving."""
    global ALLOWED_STATIC_ROOTS
    if ALLOWED_STATIC_ROOTS is None:
        ALLOWED_STATIC_ROOTS = [
            os.path.realpath(str(settings.BASE_DIR)),
            os.path.realpath(os.path.join(str(settings.BASE_DIR), 'templates', 'dist', 'spa')),
            os.path.realpath(os.path.join(str(settings.BASE_DIR), 'static')),
        ]
    return ALLOWED_STATIC_ROOTS


def _safe_file_path(base_dir, request_path):
    """
    Safely resolve a file path, preventing path traversal attacks.
    Returns the resolved path if safe, raises APIException if not.
    (SEC-010 / ISS-014)
    """
    # Resolve the full path, following symlinks
    resolved = os.path.realpath(os.path.join(base_dir, request_path.lstrip('/')))

    # Verify the resolved path is under an allowed root
    allowed_roots = _get_allowed_roots()
    if not any(resolved.startswith(root) for root in allowed_roots):
        logger.warning(f"Path traversal attempt blocked: {request_path} -> {resolved}")
        raise APIException({'detail': 'Access denied: invalid file path'})

    if not os.path.isfile(resolved):
        raise APIException({'detail': 'File not found'})

    return resolved


# SECURITY: Reasonable cache duration (PERF-005 / ISS-041)
CACHE_MAX_AGE = "max-age=86400"  # 24 hours instead of 27,397 years


def _serve_static_file(file_path):
    """Serve a static file with proper content type and caching."""
    content_type, encoding = mimetypes.guess_type(file_path)
    try:
        resp = StreamingHttpResponse(FileWrapper(open(file_path, 'rb')), content_type=content_type)
        resp['Cache-Control'] = CACHE_MAX_AGE
        return resp
    except (FileNotFoundError, PermissionError) as e:
        logger.error(f"Failed to serve file {file_path}: {e}")
        raise APIException({'detail': 'File not found'})


def robots(request):
    path = _safe_file_path(str(settings.BASE_DIR), request.path_info)
    return _serve_static_file(path)


def favicon(request):
    path = _safe_file_path(str(settings.BASE_DIR), 'static/img/logo.png')
    return _serve_static_file(path)


def css(request):
    spa_root = os.path.join(str(settings.BASE_DIR), 'templates', 'dist', 'spa')
    path = _safe_file_path(spa_root, request.path_info)
    return _serve_static_file(path)


def js(request):
    spa_root = os.path.join(str(settings.BASE_DIR), 'templates', 'dist', 'spa')
    path = _safe_file_path(spa_root, request.path_info)
    return _serve_static_file(path)


def statics(request):
    spa_root = os.path.join(str(settings.BASE_DIR), 'templates', 'dist', 'spa')
    path = _safe_file_path(spa_root, request.path_info)
    return _serve_static_file(path)


def fonts(request):
    spa_root = os.path.join(str(settings.BASE_DIR), 'templates', 'dist', 'spa')
    path = _safe_file_path(spa_root, request.path_info)
    return _serve_static_file(path)


def myip(request):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return JsonResponse({"ip": ip})
