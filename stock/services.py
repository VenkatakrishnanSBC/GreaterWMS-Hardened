"""
ARCH-001: Service layer for stock business logic.

Extracts core stock mutation operations from views into testable,
reusable service functions. Views become thin wrappers that validate
input and call these services.
"""
import logging
from typing import Optional, Dict, Any

from django.db import transaction

from .models import StockListModel, StockBinModel
from binset.models import ListModel as BinSet
from utils.md5 import Md5
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)

# Maps bin_property name → StockListModel field name
PROPERTY_FIELD_MAP: Dict[str, str] = {
    'Damage': 'damage_stock',
    'Inspection': 'inspect_stock',
    'Holding': 'hold_stock',
    'Normal': 'can_order_stock',
}


def _get_stock_field(bin_property: str) -> str:
    """
    Map a bin property name to its corresponding stock field.

    Args:
        bin_property: The bin property type ('Damage', 'Inspection', 'Holding', or 'Normal').

    Returns:
        The StockListModel field name for that property.
    """
    return PROPERTY_FIELD_MAP.get(bin_property, 'can_order_stock')


def adjust_stock_for_move(
    stock_record: StockListModel,
    from_property: str,
    to_property: str,
    qty: int,
) -> None:
    """
    Adjust stock counters when moving goods between bin properties.

    This replaces the 4×4 nested if/else matrix in the old views.py
    with a clean two-field adjustment.

    Args:
        stock_record: The StockListModel instance (must be locked via select_for_update).
        from_property: Source bin property name.
        to_property: Destination bin property name.
        qty: Number of items being moved.
    """
    if from_property == to_property:
        return  # Same property, no stock category change

    from_field = _get_stock_field(from_property)
    to_field = _get_stock_field(to_property)

    current_from = getattr(stock_record, from_field)
    current_to = getattr(stock_record, to_field)

    setattr(stock_record, from_field, current_from - qty)
    setattr(stock_record, to_field, current_to + qty)

    logger.info(
        f"Stock adjustment: {stock_record.goods_code} "
        f"{from_field}(-{qty}) → {to_field}(+{qty})"
    )


@transaction.atomic
def move_bin_stock(
    openid: str,
    stock_bin: StockBinModel,
    goods_code: str,
    bin_name: str,
    move_to_bin: str,
    move_qty: int,
) -> Dict[str, Any]:
    """
    Move stock from one bin to another.

    This is the core business logic extracted from StockBinViewSet.create().

    Args:
        openid: Tenant identifier.
        stock_bin: The source StockBinModel instance.
        goods_code: The goods code being moved.
        bin_name: Source bin name.
        move_to_bin: Destination bin name.
        move_qty: Quantity to move.

    Returns:
        Dict with operation result details.

    Raises:
        APIException: If validation fails.
    """
    if move_qty <= 0:
        raise APIException({"detail": "Move QTY Must > 0"})

    # Fetch bin configurations
    current_bin = BinSet.objects.filter(
        openid=openid, bin_name=bin_name, is_delete=False
    ).first()
    target_bin = BinSet.objects.filter(
        openid=openid, bin_name=move_to_bin, is_delete=False
    ).first()

    if not current_bin:
        raise APIException({"detail": f"Source bin '{bin_name}' not found"})
    if not target_bin:
        raise APIException({"detail": f"Target bin '{move_to_bin}' not found"})

    # Lock the stock record for update
    stock_record = StockListModel.objects.select_for_update().filter(
        openid=openid, goods_code=goods_code
    ).first()

    if not stock_record:
        raise APIException({"detail": f"Stock record for '{goods_code}' not found"})

    available_qty = stock_bin.goods_qty - stock_bin.pick_qty
    if move_qty > available_qty:
        raise APIException({"detail": "Move Qty must < Bin Goods Qty"})

    # Adjust bin quantities
    stock_bin.goods_qty -= move_qty
    if stock_bin.goods_qty == stock_bin.pick_qty == 0:
        stock_bin.delete()
    else:
        stock_bin.save()

    # Adjust stock category counters
    adjust_stock_for_move(
        stock_record, current_bin.bin_property,
        target_bin.bin_property, move_qty
    )
    stock_record.save()

    # Create new bin stock entry
    StockBinModel.objects.create(
        openid=openid,
        bin_name=move_to_bin,
        goods_code=goods_code,
        goods_desc=stock_record.goods_desc,
        goods_qty=move_qty,
        bin_size=target_bin.bin_size,
        bin_property=target_bin.bin_property,
        t_code=Md5.md5(goods_code),
    )

    # Update bin empty labels
    if target_bin.empty_label:
        target_bin.empty_label = False
        target_bin.save()

    # If source bin has no more stock, mark as empty
    if not StockBinModel.objects.filter(openid=openid, bin_name=bin_name).exists():
        current_bin.empty_label = True
        current_bin.save()

    # Cleanup zero-quantity bin records
    StockBinModel.objects.filter(
        openid=openid, goods_qty=0, pick_qty=0, picked_qty=0
    ).delete()

    logger.info(
        f"Bin move: {goods_code} x{move_qty} from {bin_name} → {move_to_bin}"
    )

    return {
        "goods_code": goods_code,
        "moved_qty": move_qty,
        "from_bin": bin_name,
        "to_bin": move_to_bin,
    }
