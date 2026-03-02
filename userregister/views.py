"""
User registration view.

CODE-005: Flattened deeply nested if/else to guard clauses.
"""
import json
import logging
import random
from typing import Any

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.models import User

from userprofile.models import Users
from utils.fbmsg import FBMsg
from utils.md5 import Md5
from staff.models import ListModel as staff

logger = logging.getLogger(__name__)


def _make_error(msg_func, ip: str, name: str) -> JsonResponse:
    """Helper to build error JsonResponse with ip and data fields."""
    err = msg_func()
    err['ip'] = ip
    err['data'] = name
    return JsonResponse(err)


def _get_client_ip(request: HttpRequest) -> str:
    """Extract client IP from request headers."""
    return (
        request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
        or request.META.get('REMOTE_ADDR', '')
    )


@csrf_exempt
def register(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    """
    Register a new user account.

    Args:
        request: HTTP POST with JSON body containing name, password1, password2.

    Returns:
        JsonResponse with success data or error message.
    """
    post_data = json.loads(request.body.decode())
    name = post_data.get('name')
    password1 = post_data.get('password1')
    password2 = post_data.get('password2')
    ip = _get_client_ip(request)

    # --- Validation ---
    if Users.objects.filter(name=str(name), developer=1, is_delete=0).exists():
        return _make_error(FBMsg.err_user_same, ip, name)

    if not password1 or str(password1) == '':
        return _make_error(FBMsg.err_password1_empty, ip, name)

    if not password2 or str(password2) == '':
        return _make_error(FBMsg.err_password2_empty, ip, name)

    if str(password1) != str(password2):
        return _make_error(FBMsg.err_password_not_same, ip, name)

    # --- Create user ---
    transaction_code = Md5.md5(name)
    user = User.objects.create_user(
        username=str(name), password=str(password1)
    )
    Users.objects.create(
        user_id=user.id, name=str(name),
        openid=transaction_code,
        appid=Md5.md5(name + '1'),
        t_code=Md5.md5(str(timezone.now())),
        developer=1, ip=ip
    )
    auth.login(request, user)

    # --- Create admin staff entry ---
    check_code = random.randint(1000, 9999)
    staff.objects.create(
        staff_name=str(name), staff_type='Admin',
        check_code=check_code, openid=transaction_code
    )
    user_id = staff.objects.filter(
        openid=transaction_code, staff_name=str(name),
        staff_type='Admin', check_code=check_code
    ).first().id

    logger.info(f"New user registered: {name} (openid={transaction_code})")

    # --- Build response ---
    ret = FBMsg.ret()
    ret['ip'] = ip
    ret['data'] = {
        'openid': transaction_code,
        'name': str(name),
        'user_id': user_id,
    }
    return JsonResponse(ret)
