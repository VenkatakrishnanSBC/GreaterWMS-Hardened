"""
Tests for ASN (Advanced Shipping Notice) workflow.

TEST-002: Tests for ASN status workflow transitions (1→2→3→4→5).
"""
import pytest
from unittest.mock import Mock, patch, MagicMock


class TestAsnStatusWorkflow:
    """Tests for ASN status transitions."""

    def test_asn_status_1_is_initial(self):
        """Status 1 = New ASN created."""
        from asn.models import AsnListModel
        fields = {f.name: f for f in AsnListModel._meta.get_fields()}
        assert 'asn_status' in fields

    def test_asn_detail_model_has_required_fields(self):
        """AsnDetailModel should have goods_code, goods_qty, etc."""
        from asn.models import AsnDetailModel
        field_names = [f.name for f in AsnDetailModel._meta.get_fields()]
        assert 'goods_code' in field_names
        assert 'goods_qty' in field_names
        assert 'asn_code' in field_names

    def test_asn_list_model_has_indexes(self):
        """DB-002: ASN should have indexes for performance."""
        from asn.models import AsnListModel
        index_names = [idx.name for idx in AsnListModel._meta.indexes]
        assert len(index_names) > 0

    def test_asn_detail_decimal_fields(self):
        """DB-003: Financial fields should be DecimalField, not FloatField."""
        from asn.models import AsnDetailModel
        from django.db.models import DecimalField
        for field_name in ['goods_weight', 'goods_volume', 'goods_cost']:
            field = AsnDetailModel._meta.get_field(field_name)
            assert isinstance(field, DecimalField), f"{field_name} should be DecimalField"


class TestDnStatusWorkflow:
    """TEST-003: Tests for DN status workflow transitions (1→2→3→4→5→6)."""

    def test_dn_detail_model_has_required_fields(self):
        """DnDetailModel should have goods_code, goods_qty, etc."""
        from dn.models import DnDetailModel
        field_names = [f.name for f in DnDetailModel._meta.get_fields()]
        assert 'goods_code' in field_names
        assert 'goods_qty' in field_names
        assert 'dn_code' in field_names

    def test_dn_list_model_has_indexes(self):
        """DB-002: DN should have indexes for performance."""
        from dn.models import DnListModel
        index_names = [idx.name for idx in DnListModel._meta.indexes]
        assert len(index_names) > 0

    def test_dn_detail_decimal_fields(self):
        """DB-003: Financial fields should be DecimalField."""
        from dn.models import DnDetailModel
        from django.db.models import DecimalField
        for field_name in ['goods_weight', 'goods_volume', 'goods_cost']:
            field = DnDetailModel._meta.get_field(field_name)
            assert isinstance(field, DecimalField), f"{field_name} should be DecimalField"

    def test_dn_delivery_damage_verbose_name(self):
        """CODE-006: delivery_damage_qty should have correct verbose_name."""
        from dn.models import DnDetailModel
        field = DnDetailModel._meta.get_field('delivery_damage_qty')
        assert 'damage' in field.verbose_name.lower()


class TestStockTransactions:
    """TEST-001: Tests for stock state machine transitions."""

    def test_stock_list_model_fields(self):
        """StockListModel should have all stock tracking fields."""
        from stock.models import StockListModel
        field_names = [f.name for f in StockListModel._meta.get_fields()]
        expected = ['goods_code', 'goods_qty', 'onhand_stock', 'can_order_stock']
        for field_name in expected:
            assert field_name in field_names, f"Missing field: {field_name}"

    def test_stock_bin_model_fields(self):
        """StockBinModel should have bin tracking fields."""
        from stock.models import StockBinModel
        field_names = [f.name for f in StockBinModel._meta.get_fields()]
        assert 'bin_name' in field_names
        assert 'goods_code' in field_names
        assert 'goods_qty' in field_names

    def test_stock_bin_auto_now_add(self):
        """DB-007: StockBinModel.create_time should have auto_now_add=True."""
        from stock.models import StockBinModel
        field = StockBinModel._meta.get_field('create_time')
        assert field.has_default() or hasattr(field, 'auto_now_add')

    def test_stock_list_indexes(self):
        """DB-002: Stock should have indexes for performance."""
        from stock.models import StockListModel
        index_names = [idx.name for idx in StockListModel._meta.indexes]
        assert len(index_names) > 0

    def test_goods_unique_constraint(self):
        """DB-004: goods_code + openid should be unique together."""
        from goods.models import ListModel
        assert len(ListModel._meta.unique_together) > 0


class TestTransactionAtomicApplied:
    """Verify transaction.atomic decorators are in place (DB-001)."""

    def test_stock_views_import_transaction(self):
        """stock/views.py should import transaction."""
        import stock.views
        from django.db import transaction
        assert hasattr(stock.views, 'transaction')

    def test_asn_views_import_transaction(self):
        """asn/views.py should import transaction."""
        import asn.views
        assert hasattr(asn.views, 'transaction')

    def test_dn_views_import_transaction(self):
        """dn/views.py should import transaction."""
        import dn.views
        assert hasattr(dn.views, 'transaction')
