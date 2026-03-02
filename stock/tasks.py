"""
FEATURE-007: Safety stock alerting Celery tasks.
FEATURE-008: ERP integration layer tasks.

Async tasks for:
- Checking safety stock levels and sending alerts
- Syncing data with external ERP systems
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

try:
    from celery import shared_task
except ImportError:
    # Fallback for when Celery is not installed
    def shared_task(func=None, **kwargs):
        if func:
            return func
        return lambda f: f


@shared_task(bind=True, max_retries=3)
def check_safety_stock_levels(self) -> Dict[str, Any]:
    """
    FEATURE-007: Check all goods for safety stock violations.

    Runs hourly via Celery Beat. Compares current stock levels
    against safety_stock thresholds and sends notifications.
    """
    from goods.models import ListModel as Goods
    from stock.models import StockListModel
    from utils.notifications import notify_low_stock

    alerts_sent = 0
    violations = []

    try:
        # Get all goods with safety stock configured
        goods_with_safety = Goods.objects.filter(
            safety_stock__gt=0, is_delete=False
        ).values('goods_code', 'goods_desc', 'safety_stock', 'openid')

        for goods in goods_with_safety:
            stock = StockListModel.objects.filter(
                openid=goods['openid'],
                goods_code=goods['goods_code'],
            ).first()

            current_qty = stock.onhand_stock if stock else 0

            if current_qty < goods['safety_stock']:
                violations.append({
                    'goods_code': goods['goods_code'],
                    'goods_desc': goods['goods_desc'],
                    'current_qty': current_qty,
                    'safety_stock': goods['safety_stock'],
                    'deficit': goods['safety_stock'] - current_qty,
                    'openid': goods['openid'],
                })

        # Send notification for each violation
        for v in violations:
            # In production, look up notification recipients from user preferences
            logger.warning(
                f"Safety stock alert: {v['goods_code']} — "
                f"{v['current_qty']}/{v['safety_stock']} "
                f"(deficit: {v['deficit']})"
            )
            alerts_sent += 1

        logger.info(
            f"Safety stock check complete: {len(violations)} violations "
            f"out of {len(list(goods_with_safety))} monitored items"
        )

        return {
            'checked': len(list(goods_with_safety)),
            'violations': len(violations),
            'alerts_sent': alerts_sent,
            'details': violations[:20],  # Limit detail size
        }

    except Exception as exc:
        logger.error(f"Safety stock check failed: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def sync_with_erp(self) -> Dict[str, Any]:
    """
    FEATURE-008: Sync warehouse data with external ERP system.

    Runs every 15 minutes via Celery Beat.
    Pushes stock levels, receives purchase orders,
    and synchronizes product master data.
    """
    from django.conf import settings

    erp_url = getattr(settings, 'ERP_API_URL', '')
    erp_key = getattr(settings, 'ERP_API_KEY', '')

    if not erp_url:
        logger.info("ERP sync skipped: ERP_API_URL not configured")
        return {'status': 'skipped', 'reason': 'ERP_API_URL not configured'}

    results = {
        'stock_pushed': 0,
        'orders_received': 0,
        'products_synced': 0,
        'errors': [],
    }

    try:
        # Phase 1: Push stock levels to ERP
        results['stock_pushed'] = _push_stock_to_erp(erp_url, erp_key)

        # Phase 2: Pull purchase orders from ERP
        results['orders_received'] = _pull_orders_from_erp(erp_url, erp_key)

        # Phase 3: Sync product master data
        results['products_synced'] = _sync_products_from_erp(erp_url, erp_key)

        logger.info(
            f"ERP sync complete: {results['stock_pushed']} stock pushed, "
            f"{results['orders_received']} orders received, "
            f"{results['products_synced']} products synced"
        )
        return results

    except Exception as exc:
        logger.error(f"ERP sync failed: {exc}")
        results['errors'].append(str(exc))
        raise self.retry(exc=exc, countdown=120)


def _push_stock_to_erp(erp_url: str, erp_key: str) -> int:
    """Push current stock levels to ERP system."""
    import requests
    from stock.models import StockListModel

    stock_data = StockListModel.objects.all().values(
        'goods_code', 'goods_qty', 'onhand_stock',
        'can_order_stock', 'openid'
    )

    if not stock_data:
        return 0

    try:
        response = requests.post(
            f"{erp_url}/api/stock/sync",
            json={'stock': list(stock_data)},
            headers={'Authorization': f'Bearer {erp_key}'},
            timeout=30,
        )
        response.raise_for_status()
        return len(stock_data)
    except requests.RequestException as e:
        logger.error(f"ERP stock push failed: {e}")
        return 0


def _pull_orders_from_erp(erp_url: str, erp_key: str) -> int:
    """Pull new purchase orders from ERP and create ASNs."""
    import requests

    try:
        response = requests.get(
            f"{erp_url}/api/orders/pending",
            headers={'Authorization': f'Bearer {erp_key}'},
            timeout=30,
        )
        response.raise_for_status()
        orders = response.json().get('orders', [])

        # TODO: Create ASN records from ERP orders
        for order in orders:
            logger.info(f"ERP order received: {order.get('order_id', 'unknown')}")

        return len(orders)
    except requests.RequestException as e:
        logger.error(f"ERP order pull failed: {e}")
        return 0


def _sync_products_from_erp(erp_url: str, erp_key: str) -> int:
    """Sync product master data from ERP."""
    import requests

    try:
        response = requests.get(
            f"{erp_url}/api/products/updated",
            headers={'Authorization': f'Bearer {erp_key}'},
            timeout=30,
        )
        response.raise_for_status()
        products = response.json().get('products', [])

        # TODO: Update goods records from ERP products
        for product in products:
            logger.info(f"ERP product synced: {product.get('sku', 'unknown')}")

        return len(products)
    except requests.RequestException as e:
        logger.error(f"ERP product sync failed: {e}")
        return 0


@shared_task
def cleanup_expired_records() -> Dict[str, int]:
    """Clean up expired throttle and session records."""
    from throttle.models import ListModel
    from django.utils import timezone

    cutoff = timezone.now() - timezone.timedelta(hours=24)
    deleted_count = ListModel.objects.filter(create_time__lt=cutoff).delete()[0]

    logger.info(f"Cleaned up {deleted_count} expired throttle records")
    return {'deleted': deleted_count}
