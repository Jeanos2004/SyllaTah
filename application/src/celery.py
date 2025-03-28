import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = Celery('SyllaTah')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configure Celery to use the memory transport
app.conf.update(
    broker_url='memory:///',
    result_backend='cache+memory:///',
    task_always_eager=True,
    task_eager_propagates=True,
)

from celery.schedules import crontab

app.conf.beat_schedule = {
    'clean-monitoring-logs': {
        'task': 'core.tasks.clean_monitoring_logs',
        'schedule': crontab(day_of_week='sunday', hour=0, minute=0),
    },
}