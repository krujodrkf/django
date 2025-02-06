from celery import shared_task
import requests
from django.conf import settings
from django.db import connection  # Importar conexión a la base de datos

@shared_task
def update_country_data():
    """
    Tarea para obtener y guardar los datos de los países desde el endpoint.
    Se ejecuta periódicamente y usa advisory locks para evitar ejecuciones simultáneas.
    """
    url = f"{settings.API_BASE_URL}/api/countries/"  # URL base definida en settings.py
    lock_id = 12345  # ID único para el advisory lock
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_try_advisory_lock(%s)", [lock_id])
        locked = cursor.fetchone()[0]
        
        if not locked:
            print("Otra instancia de la tarea ya está ejecutándose. Abortando.")
            return  # Sale si ya hay otra tarea corriendo

        try:
            print("Obteniendo datos de países...")
            response = requests.get(url)
            response.raise_for_status()
            countries_data = response.json()
            print("Datos de países obtenidos:", countries_data)
            
            # Aquí puedes procesar y almacenar los datos en la base de datos

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener los datos de países: {e}")
        finally:
            cursor.execute("SELECT pg_advisory_unlock(%s)", [lock_id])  # Libera el bloqueo
