import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'DjangoProjectNewsPortal.settings')
app = Celery('DjangoProjectNewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_massage_post_every_monday_8am': {
        'task': 'board.tasks.send_massage_post_every_monday_8am',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

