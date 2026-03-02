---
name: testing-strategy
description: Testing framework setup — pytest, factories, fixtures, coverage, and CI integration
---

# Testing Strategy Skill

Use this skill when implementing TODO items TEST-001 through TEST-010 or fixing issues ISS-015, ISS-016.

## 1. Framework Setup

```bash
# Install test dependencies:
pip install pytest pytest-django factory-boy coverage pytest-cov faker
```

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "greaterwms.settings"
python_files = ["tests/*.py", "test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=80"
markers = [
    "unit: Unit tests (fast)",
    "integration: Integration tests (DB required)",
    "slow: Slow tests",
]
```

## 2. Model Factories (factory-boy)

```python
# tests/factories.py
import factory
from userprofile.models import Users
from goods.models import ListModel as GoodsListModel
from stock.models import StockListModel

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users
    openid = factory.LazyFunction(lambda: f"test-{factory.Faker('uuid4').evaluate(None, None, {})}")
    appid = factory.Faker('uuid4')
    user_id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('name')

class GoodsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoodsListModel
    goods_code = factory.Sequence(lambda n: f"SKU-{n:05d}")
    goods_desc = factory.Faker('sentence', nb_words=4)
    goods_supplier = factory.Faker('company')
    goods_weight = factory.Faker('pydecimal', min_value=0.1, max_value=100)
    openid = factory.LazyAttribute(lambda o: UserFactory().openid)

class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockListModel
    goods_code = factory.LazyAttribute(lambda o: GoodsFactory().goods_code)
    goods_qty = 100
    onhand_stock = 100
    openid = factory.LazyAttribute(lambda o: UserFactory().openid)
```

## 3. Test Examples

### Stock State Machine Tests (P0)
```python
# stock/tests/test_stock_state.py
import pytest
from tests.factories import StockFactory

@pytest.mark.unit
class TestStockStateMachine:
    def test_asn_increases_asn_stock(self):
        stock = StockFactory(asn_stock=0)
        stock.asn_stock += 10
        stock.save()
        stock.refresh_from_db()
        assert stock.asn_stock == 10

    def test_stock_cannot_go_negative(self):
        stock = StockFactory(onhand_stock=5)
        with pytest.raises(ValueError):
            # Should validate, not silently clamp to 0
            stock.onhand_stock -= 10
            stock.save()
```

### API Integration Tests
```python
# asn/tests/test_asn_api.py
import pytest
from rest_framework.test import APIClient
from tests.factories import UserFactory

@pytest.mark.integration
class TestAsnAPI:
    @pytest.fixture
    def authenticated_client(self):
        user = UserFactory()
        client = APIClient()
        client.credentials(HTTP_TOKEN=user.openid)
        return client, user

    def test_create_asn(self, authenticated_client):
        client, user = authenticated_client
        response = client.post('/asn/', {'supplier': 'Test Supplier'})
        assert response.status_code == 201
```

## 4. Coverage Configuration

```ini
# .coveragerc
[run]
source = .
omit =
    */migrations/*
    */tests/*
    manage.py
    greaterwms/asgi.py
    greaterwms/wsgi.py

[report]
fail_under = 80
show_missing = True
```

## 5. CI Integration

```yaml
# In .github/workflows/ci.yml:
- name: Run tests with coverage
  run: |
    pytest --cov --cov-report=xml --cov-fail-under=80
```

## Priority Test Order
1. Stock state machine (most critical business logic)
2. ASN status workflow (1→2→3→4→5)
3. DN status workflow (1→2→3→4→5→6)
4. Authentication/authorization
5. Data validation utilities
6. API endpoint CRUD operations
