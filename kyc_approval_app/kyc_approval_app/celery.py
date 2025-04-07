import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kyc_approval_app.settings")

app = Celery("kyc_approval_app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
