import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "github_repos.settings")

app = Celery("github_repos")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

celery = app