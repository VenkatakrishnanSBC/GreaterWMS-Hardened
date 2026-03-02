---
name: database-optimization
description: Database schema improvements — indexes, transactions, ForeignKeys, DecimalField, migrations
---

# Database Optimization Skill

Use this skill when fixing database issues (ISS-009 through ISS-012, ISS-019, ISS-029) or implementing TODO items DB-001 through DB-008.

## 1. Add Database Transactions

```python
from django.db import transaction

# Wrap multi-model operations:
class AsnSortedViewSet(viewsets.ModelViewSet):
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # All DB operations inside here are atomic
        # On ANY exception, everything rolls back
        stock = StockListModel.objects.select_for_update().get(...)
        stock.asn_stock -= qty
        stock.onhand_stock += qty
        stock.save()
```

## 2. Add Database Indexes

```python
class AsnListModel(models.Model):
    class Meta:
        db_table = 'asnlist'
        indexes = [
            models.Index(fields=['openid', 'is_delete']),
            models.Index(fields=['openid', 'asn_code']),
            models.Index(fields=['openid', 'asn_status']),
        ]

# Apply pattern to ALL models: always index (openid, is_delete)
# Plus any frequently filtered field
```

## 3. Convert FloatField to DecimalField

```python
# Before (BAD):
goods_cost = models.FloatField(default=0)

# After (GOOD):
goods_cost = models.DecimalField(max_digits=12, decimal_places=4, default=0)

# Migration strategy:
# 1. Add new DecimalField alongside FloatField
# 2. Data migration to copy values
# 3. Remove old FloatField
# 4. Rename new field to original name
```

## 4. Convert String References to ForeignKeys

```python
# Before (BAD):
supplier = models.CharField(max_length=255, verbose_name="Supplier")

# After (GOOD):
supplier = models.ForeignKey(
    'supplier.ListModel',
    on_delete=models.PROTECT,
    related_name='asn_details',
    verbose_name="Supplier"
)

# Migration strategy:
# 1. Add nullable ForeignKey
# 2. Data migration to link by name
# 3. Make ForeignKey non-null
# 4. Remove old CharField
```

## 5. Add Concurrency Control

```python
# Option A: Pessimistic locking
with transaction.atomic():
    stock = StockListModel.objects.select_for_update().get(
        openid=openid, goods_code=goods_code
    )
    stock.onhand_stock -= qty
    stock.save()

# Option B: Optimistic locking (add version field)
class StockListModel(models.Model):
    version = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.version += 1
        super().save(*args, **kwargs)
```

## Verification
```bash
# Check for pending migrations:
python manage.py makemigrations --check --dry-run

# Apply migrations:
python manage.py migrate

# Verify indexes exist:
python manage.py dbshell
# Then: .indexes (SQLite) or \di (PostgreSQL)
```
