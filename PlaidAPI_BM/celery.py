import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PlaidAPI_BM.settings')

app = Celery('PlaidAPI_BM')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()