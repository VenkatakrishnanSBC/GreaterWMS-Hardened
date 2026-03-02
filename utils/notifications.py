"""
FEATURE-002: Notification service for GreaterWMS.

Supports email and SMS notifications for warehouse events like:
- Low stock alerts (FEATURE-007)
- ASN/DN status changes
- Order completion notifications
- User registration confirmations
"""
import logging
from typing import List, Optional, Dict, Any

from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class NotificationType:
    """Notification event types."""
    LOW_STOCK = 'low_stock'
    ASN_RECEIVED = 'asn_received'
    ASN_SORTED = 'asn_sorted'
    DN_SHIPPED = 'dn_shipped'
    DN_DELIVERED = 'dn_delivered'
    ORDER_COMPLETE = 'order_complete'
    USER_REGISTERED = 'user_registered'
    SAFETY_STOCK_ALERT = 'safety_stock_alert'
    ERP_SYNC_FAILED = 'erp_sync_failed'


def send_email_notification(
    subject: str,
    message: str,
    recipient_list: List[str],
    html_message: Optional[str] = None,
) -> bool:
    """
    Send an email notification.

    Args:
        subject: Email subject line.
        message: Plain text message body.
        recipient_list: List of recipient email addresses.
        html_message: Optional HTML message body.

    Returns:
        True if the email was sent successfully.
    """
    try:
        sent = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email sent to {recipient_list}: {subject}")
        return sent > 0
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_list}: {e}")
        return False


def send_bulk_notifications(
    notifications: List[Dict[str, Any]],
) -> int:
    """
    Send multiple email notifications efficiently.

    Args:
        notifications: List of dicts with keys: subject, message, from_email, recipient_list.

    Returns:
        Number of emails successfully sent.
    """
    messages = [
        (
            n['subject'],
            n['message'],
            n.get('from_email', settings.DEFAULT_FROM_EMAIL),
            n['recipient_list'],
        )
        for n in notifications
    ]
    try:
        sent = send_mass_mail(messages, fail_silently=False)
        logger.info(f"Bulk notification: {sent}/{len(messages)} emails sent")
        return sent
    except Exception as e:
        logger.error(f"Bulk notification failed: {e}")
        return 0


def notify_low_stock(
    goods_code: str,
    goods_desc: str,
    current_qty: int,
    safety_stock: int,
    recipients: List[str],
) -> bool:
    """
    FEATURE-007: Send low stock alert notification.

    Args:
        goods_code: The goods code that is low.
        goods_desc: Description of the goods.
        current_qty: Current stock quantity.
        safety_stock: Safety stock threshold.
        recipients: List of email addresses to notify.

    Returns:
        True if notification was sent.
    """
    subject = f"⚠️ Low Stock Alert: {goods_code}"
    message = (
        f"Low Stock Alert\n\n"
        f"Goods: {goods_code} - {goods_desc}\n"
        f"Current Stock: {current_qty}\n"
        f"Safety Stock Level: {safety_stock}\n"
        f"Deficit: {safety_stock - current_qty} units\n\n"
        f"Please reorder immediately."
    )
    return send_email_notification(subject, message, recipients)


def notify_asn_status_change(
    asn_code: str,
    old_status: int,
    new_status: int,
    recipients: List[str],
) -> bool:
    """Notify stakeholders when ASN status changes."""
    status_names = {1: 'Created', 2: 'Confirmed', 3: 'Received', 4: 'Sorted', 5: 'Complete'}
    subject = f"ASN {asn_code}: {status_names.get(new_status, 'Updated')}"
    message = (
        f"ASN Status Update\n\n"
        f"ASN Code: {asn_code}\n"
        f"Status: {status_names.get(old_status, old_status)} → "
        f"{status_names.get(new_status, new_status)}\n"
    )
    return send_email_notification(subject, message, recipients)


def notify_dn_status_change(
    dn_code: str,
    old_status: int,
    new_status: int,
    recipients: List[str],
) -> bool:
    """Notify stakeholders when DN status changes."""
    status_names = {
        1: 'Created', 2: 'Confirmed', 3: 'Picking',
        4: 'Picked', 5: 'Shipped', 6: 'Delivered'
    }
    subject = f"DN {dn_code}: {status_names.get(new_status, 'Updated')}"
    message = (
        f"DN Status Update\n\n"
        f"DN Code: {dn_code}\n"
        f"Status: {status_names.get(old_status, old_status)} → "
        f"{status_names.get(new_status, new_status)}\n"
    )
    return send_email_notification(subject, message, recipients)
