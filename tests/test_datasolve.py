"""
Tests for utils/datasolve.py — Input validation functions.

TEST-004: Unit tests for data validation utilities.
"""
import pytest
from rest_framework.exceptions import APIException


class TestDataValidate:
    """Tests for the data_validate function."""

    def test_valid_data_passes(self):
        from utils.datasolve import data_validate
        assert data_validate("hello") == "hello"

    def test_valid_number_passes(self):
        from utils.datasolve import data_validate
        assert data_validate(42) == 42

    def test_none_raises_exception(self):
        from utils.datasolve import data_validate
        with pytest.raises(APIException):
            data_validate(None)

    def test_script_keyword_now_allowed(self):
        """After SEC-009 fix, 'script' in data should be allowed (it's not XSS in API)."""
        from utils.datasolve import data_validate
        result = data_validate("JavaScript tutorial")
        assert result == "JavaScript tutorial"

    def test_select_keyword_now_allowed(self):
        """After SEC-009 fix, 'select' in data should be allowed (Django ORM prevents SQLi)."""
        from utils.datasolve import data_validate
        result = data_validate("Please select an option")
        assert result == "Please select an option"


class TestQtyValidation:
    """Tests for quantity validation functions."""

    def test_qty_0_valid_positive(self):
        from utils.datasolve import qty_0_data_validate
        assert qty_0_data_validate(5) == 5

    def test_qty_0_rejects_zero(self):
        from utils.datasolve import qty_0_data_validate
        with pytest.raises(APIException):
            qty_0_data_validate(0)

    def test_qty_0_rejects_negative(self):
        from utils.datasolve import qty_0_data_validate
        with pytest.raises(APIException):
            qty_0_data_validate(-1)

    def test_qty_0_rejects_none(self):
        from utils.datasolve import qty_0_data_validate
        with pytest.raises(APIException):
            qty_0_data_validate(None)

    def test_qty_valid_zero(self):
        from utils.datasolve import qty_data_validate
        assert qty_data_validate(0) == 0

    def test_qty_valid_positive(self):
        from utils.datasolve import qty_data_validate
        assert qty_data_validate(10) == 10

    def test_qty_rejects_negative(self):
        from utils.datasolve import qty_data_validate
        with pytest.raises(APIException):
            qty_data_validate(-5)

    def test_qty_string_number(self):
        from utils.datasolve import qty_0_data_validate
        assert qty_0_data_validate("5") == 5


class TestAsnDnCodeGeneration:
    """Tests for ASN and DN code generation."""

    def test_asn_first_code(self):
        from utils.datasolve import asn_data_validate
        result = asn_data_validate("ASN00000001")
        assert result == "ASN00000001"

    def test_asn_increment(self):
        from utils.datasolve import asn_data_validate
        result = asn_data_validate("ASN00000005")
        assert result == "ASN00000006"

    def test_asn_none_returns_default(self):
        from utils.datasolve import asn_data_validate
        with pytest.raises(APIException):
            asn_data_validate(None)

    def test_dn_first_code(self):
        from utils.datasolve import dn_data_validate
        result = dn_data_validate("DN00000001")
        assert result == "DN00000001"

    def test_dn_increment(self):
        from utils.datasolve import dn_data_validate
        result = dn_data_validate("DN00000099")
        assert result == "DN00000100"


class TestSumOfList:
    """Tests for the refactored sumOfList function (ARCH-007)."""

    def test_sum_full_list(self):
        from utils.datasolve import sumOfList
        assert sumOfList([1, 2, 3, 4, 5], 5) == 15

    def test_sum_partial_list(self):
        from utils.datasolve import sumOfList
        assert sumOfList([1, 2, 3, 4, 5], 3) == 6

    def test_sum_empty(self):
        from utils.datasolve import sumOfList
        assert sumOfList([1, 2, 3], 0) == 0


class TestIsNumber:
    """Tests for is_number utility."""

    def test_integer(self):
        from utils.datasolve import is_number
        assert is_number("42") is True

    def test_float(self):
        from utils.datasolve import is_number
        assert is_number("3.14") is True

    def test_string(self):
        from utils.datasolve import is_number
        assert is_number("hello") is False

    def test_none(self):
        from utils.datasolve import is_number
        assert is_number(None) is False


class TestTransportationCalculate:
    """Tests for transportation cost calculation."""

    def test_weight_dominant(self):
        from utils.datasolve import transportation_calculate
        result = transportation_calculate(
            weight=100, volume=10, weight_fee=2, volume_fee=1, min_fee=50
        )
        assert result == 200.0  # weight_cost = 200 > volume_cost = 10 > min = 50

    def test_volume_dominant(self):
        from utils.datasolve import transportation_calculate
        result = transportation_calculate(
            weight=10, volume=100, weight_fee=1, volume_fee=3, min_fee=50
        )
        assert result == 300.0  # volume_cost = 300 > weight_cost = 10 > min = 50

    def test_minimum_fee_applied(self):
        from utils.datasolve import transportation_calculate
        result = transportation_calculate(
            weight=1, volume=1, weight_fee=1, volume_fee=1, min_fee=100
        )
        assert result == 100.0  # min_fee > both costs

    def test_rounding(self):
        from utils.datasolve import transportation_calculate
        result = transportation_calculate(
            weight=1, volume=1, weight_fee=1.111, volume_fee=1.222, min_fee=0
        )
        assert result == 1.22  # Rounded to 2 decimal places


class TestBarCode:
    """Tests for barcode encode/decode."""

    def test_encode_decode_roundtrip(self):
        from utils.datasolve import secret_bar_code, verify_bar_code
        import json
        data = {"goods_code": "SKU001", "qty": 10}
        encoded = secret_bar_code(json.dumps(data))
        decoded = verify_bar_code(encoded)
        assert decoded["goods_code"] == "SKU001"
        assert decoded["qty"] == 10
