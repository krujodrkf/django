from __future__ import absolute_import, unicode_literals

# Se asegura de que la aplicación Celery se cargue cuando Django se inicie
from .celery import app as celery_app

__all__ = ('celery_app',)