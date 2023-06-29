import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobify.settings')

app = Celery('Jobify')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send-selected_email': {
        'task': 'company.tasks.send_selected_email_task',
        'schedule': crontab(minute='*/1')
    }

}
app.autodiscover_tasks()
