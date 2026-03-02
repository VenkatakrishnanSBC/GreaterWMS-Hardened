---
name: api-refactoring
description: REST API improvements — service layer extraction, versioning, pagination, response format unification
---

# API Refactoring Skill

Use this skill when implementing TODO items ARCH-001 through ARCH-007 or fixing issues ISS-020, ISS-021, ISS-037, ISS-038, ISS-045.

## 1. Service Layer Extraction

Create a `services.py` in each app to separate business logic from views:

```python
# asn/services.py
from django.db import transaction
from asn.models import AsnListModel, AsnDetailModel
from stock.models import StockListModel

class AsnService:
    @staticmethod
    @transaction.atomic
    def create_asn(openid: str, supplier: str, details: list[dict]) -> AsnListModel:
        """Create an ASN with detail lines."""
        asn = AsnListModel.objects.create(
            openid=openid,
            asn_code=AsnService._generate_code(openid),
            supplier=supplier,
            asn_status=1,
        )
        for detail in details:
            AsnDetailModel.objects.create(asn_code=asn.asn_code, **detail)
        return asn

    @staticmethod
    def transition_status(asn_code: str, from_status: int, to_status: int) -> None:
        """Transition ASN through status with validation."""
        asn = AsnListModel.objects.get(asn_code=asn_code)
        if asn.asn_status != from_status:
            raise ValueError(f"ASN {asn_code} is in status {asn.asn_status}, expected {from_status}")
        asn.asn_status = to_status
        asn.save()

# asn/views.py — now thin:
class AsnListViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        asn = AsnService.create_asn(
            openid=request.auth.openid,
            supplier=request.data.get('supplier'),
            details=request.data.get('details', []),
        )
        return Response(AsnListSerializer(asn).data, status=201)
```

## 2. API Versioning

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}

# urls.py
urlpatterns = [
    path('api/v1/', include('api_v1.urls')),
    path('api/v2/', include('api_v2.urls')),
]
```

## 3. Default Pagination

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'utils.page.MyPageNumberPagination',
    'PAGE_SIZE': 30,
}
```

## 4. Unified Response Format

```python
# utils/response.py
from rest_framework.response import Response

def success_response(data=None, message="Success", status=200):
    return Response({
        "status": status,
        "message": message,
        "data": data,
    }, status=status)

def error_response(message="Error", errors=None, status=400):
    return Response({
        "status": status,
        "message": message,
        "errors": errors,
    }, status=status)
```

## 5. Refactor Throttle (DRY)

```python
# utils/throttle.py — unified method handler
class VisitThrottle(BaseThrottle):
    def allow_request(self, request, view):
        method = request.method.upper()
        throttle_setting = getattr(settings, f'{method}_THROTTLE', 500)
        return self._check_rate(request, method, throttle_setting)

    def _check_rate(self, request, method, limit):
        ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        # Single implementation for all methods
        ...
```

## Verification
- All API endpoints return consistent response format
- Pagination works on all list endpoints
- API version prefix in URLs
- No business logic remaining in views (only service calls)
