"""
UPGRADE-004: Celery application configuration for GreaterWMS.

Enables async task processing for long-running operations like:
- PDF report generation (FEATURE-003)
- Email/SMS notifications (FEATURE-002)
- Bulk stock recalculation
- ERP synchronization (FEATURE-008)

Usage:
    Set CELERY_BROKER_URL env var (e.g., redis://localhost:6379/2)
    Start worker: celery -A greaterwms worker -l info
    Start beat:   celery -A greaterwms beat -l info
"""
import os

from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greaterwms.settings')

app = Celery('greaterwms')

# Load config from Django settings, namespace='CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Periodic task schedule (Celery Beat)
app.conf.beat_schedule = {
    # FEATURE-007: Safety stock check every hour
    'check-safety-stock': {
        'task': 'stock.tasks.check_safety_stock_levels',
        'schedule': crontab(minute=0),  # Every hour
    },
    # Clean up expired throttle records daily
    'cleanup-throttle-records': {
        'task': 'throttle.tasks.cleanup_expired_records',
        'schedule': crontab(hour=3, minute=0),  # 3 AM daily
    },
    # FEATURE-008: ERP sync every 15 minutes
    'erp-sync': {
        'task': 'erp.tasks.sync_with_erp',
        'schedule': crontab(minute='*/15'),  # Every 15 min
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to verify Celery is working."""
    print(f'Request: {self.request!r}')
