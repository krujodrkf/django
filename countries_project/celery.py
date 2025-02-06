from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'countries_project.settings')# Usar la configuración de Django

app = Celery('countries_project')
app.config_from_object('django.conf:settings', namespace='CELERY')# Usar los settings de Django para la configuración de Celery
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) # Descubrir las tareas en todas las aplicaciones instaladas
app.conf.timezone = 'UTC'
