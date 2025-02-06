from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta  # Importa timedelta para usarlo en el horario
from django.conf import settings

# Usar la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'countries_project.settings')

app = Celery('countries_project')

# Usar los settings de Django para la configuración de Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir las tareas en todas las aplicaciones instaladas
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Configurar la programación de Celery Beat usando timedelta
app.conf.beat_schedule = {
    'update-country-data-every-5-seconds': {
        'task': 'countries_project.tasks.update_country_data',
        'schedule': timedelta(seconds=5),  # Ejecutar cada 5 segundos usando timedelta
    },
}

# Establecer maxinterval en 1 segundo o el valor deseado (especificado en segundos)
app.conf.beat_max_loop_interval = 5  # Esto asegura que Celery Beat no limite la ejecución a 5 minutos

# Habilitar una frecuencia de ejecución menor de 5 minutos
app.conf.timezone = 'UTC'
