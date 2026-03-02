from userprofile.models import Users
import re
import base64
import json
import logging
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


# SECURITY: Proper input validation (SEC-009 / ISS-024)
# Removed naive regex-based XSS/SQLi checks that:
#   1. Were trivially bypassable
#   2. Blocked legitimate data (e.g., products named "Select" or "JavaScript")
# Django ORM already prevents SQL injection via parameterized queries.
# For HTML content, use bleach or Django's escape utilities if needed.

def data_validate(data):
    """Validate general data input. Returns the data if valid."""
    if data is None:
        raise APIException({'detail': 'Data cannot be empty'})
    return data


def qty_0_data_validate(data):
    """Validate quantity must be greater than 0."""
    if data is None:
        raise APIException({'detail': 'Quantity cannot be empty'})
    try:
        val = int(data) if isinstance(data, str) else data
    except (ValueError, TypeError):
        raise APIException({'detail': 'Quantity must be a number'})
    if val > 0:
        return val
    else:
        raise APIException({'detail': 'Qty Must > 0'})


def qty_data_validate(data):
    """Validate quantity must be greater than or equal to 0."""
    if data is None:
        raise APIException({'detail': 'Quantity cannot be empty'})
    try:
        val = int(data) if isinstance(data, str) else data
    except (ValueError, TypeError):
        raise APIException({'detail': 'Quantity must be a number'})
    if val >= 0:
        return val
    else:
        raise APIException({'detail': 'Qty Must >= 0'})


def openid_validate(data):
    """Validate that the openid exists in the system."""
    if not data or not isinstance(data, str):
        raise APIException({'detail': 'Invalid openid'})
    if Users.objects.filter(openid=data).exists():
        return data
    else:
        raise APIException({'detail': 'User does not exists'})


def appid_validate(data):
    """Validate that the appid exists in the system."""
    if not data or not isinstance(data, str):
        raise APIException({'detail': 'Invalid appid'})
    if Users.objects.filter(appid=data).exists():
        return data
    else:
        raise APIException({'detail': 'User does not exists'})


def asn_data_validate(data):
    """Generate next ASN code from the last code."""
    if data is None:
        raise APIException({'detail': 'ASN data cannot be empty'})
    asn_last_code = re.findall(r'\d+', str(data), re.IGNORECASE)
    if not asn_last_code:
        return 'ASN00000001'
    if str(asn_last_code[0]) == '00000001':
        data = 'ASN' + '00000001'
    else:
        data = 'ASN' + str(int(asn_last_code[0]) + 1).zfill(8)
    return data


def dn_data_validate(data):
    """Generate next DN code from the last code."""
    if data is None:
        raise APIException({'detail': 'DN data cannot be empty'})
    dn_last_code = re.findall(r'\d+', str(data), re.IGNORECASE)
    if not dn_last_code:
        return 'DN00000001'
    if str(dn_last_code[0]) == '00000001':
        data = 'DN' + '00000001'
    else:
        data = 'DN' + str(int(dn_last_code[0]) + 1).zfill(8)
    return data


def sumOfList(list, size):
    """Sum a list of numbers. Uses built-in sum() instead of recursion (ARCH-007)."""
    return sum(list[:size])


def is_number(data):
    """Check if data can be converted to a number."""
    try:
        float(data)
        return True
    except (ValueError, TypeError):
        return False


def secret_bar_code(data):
    """Encode data as a base64 barcode."""
    return base64.b64encode(str(data).encode()).decode()


def verify_bar_code(data):
    """Decode a base64 barcode back to data."""
    try:
        return json.loads(base64.b64decode(str(data).encode()).decode().replace('\'', '\"'))
    except (json.JSONDecodeError, Exception) as e:
        logger.warning(f"Failed to verify barcode: {e}")
        raise APIException({'detail': 'Invalid barcode data'})


def transportation_calculate(weight, volume, weight_fee, volume_fee, min_fee):
    """Calculate transportation cost based on weight, volume, and minimum fee."""
    weight_cost = weight * weight_fee
    volume_cost = volume * volume_fee
    max_cost = max(weight_cost, volume_cost, min_fee)
    return round(max_cost, 2)
