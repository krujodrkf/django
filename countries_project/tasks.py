from celery import shared_task
import requests
from django.conf import settings  # Importa settings

@shared_task
def update_country_data():
    """
    Tarea para obtener y guardar los datos de los países desde el endpoint.
    Se puede ejecutar periódicamente (por ejemplo, cada hora).
    """
    # Usa la URL base definida en settings.py
    print ("szdfasf")
    url = f"{settings.API_BASE_URL}/api/countries/"  # Combina la URL base con el endpoint

    try:
        # Realizar solicitud GET al endpoint
        response = requests.get(url)
        response.raise_for_status()  # Levanta un error si la respuesta no es exitosa (status 200)
        
        # Aquí deberías agregar la lógica para procesar y guardar los datos en tu base de datos.
        countries_data = response.json()
        print("Datos de países obtenidos:", countries_data)
        
        # Lógica de almacenamiento de los datos en la base de datos
        # Por ejemplo: para cada país en los datos, guardarlo en la base de datos.

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos de países: {e}")
