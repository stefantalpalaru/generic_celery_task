import celery
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
app = celery.Celery()
app.config_from_object('celeryconfig')

from generic_celery_task.decorators import task

