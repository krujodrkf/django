from django.db import transaction
from time import sleep
import requests
from rest_framework.response import Response
from rest_framework import status
from api.models import Country
from celery import shared_task

@shared_task
def update_country_data():
    """
    Función que obtiene la lista de países desde el endpoint externo
    https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng
    y guarda los datos en la base de datos sin duplicados y validando los datos.
    """
    url = "https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng"
    error_messages = []
    retries = 3
    retry_delay = 5

    for attempt in range(retries):
        try:
            with transaction.atomic():
                transaction.on_commit(lambda: transaction.get_connection().cursor().execute("SELECT pg_advisory_lock(123456)"))
                respuesta = requests.get(url)
                respuesta.raise_for_status()
                data = respuesta.json()

                for country_data in data:
                    if not country_data.get('name') or not country_data['name'].get('common'):
                        error_messages.append(f"Faltan datos para el país {country_data.get('name', {}).get('common', 'desconocido')}")
                        continue

                    capital = country_data.get('capital')
                    if capital and not isinstance(capital[0], str):
                        error_messages.append(f"Capital no válida para el país {country_data['name']['common']}")
                        continue

                    if not isinstance(country_data.get('population', 0), int):
                        error_messages.append(f"Población no válida para el país {country_data['name']['common']}")
                        continue

                    latlng = country_data.get('latlng', [])
                    if len(latlng) != 2 or not all(isinstance(coord, (float, int)) for coord in latlng):
                        error_messages.append(f"Coordenadas no válidas para el país {country_data['name']['common']}")
                        continue

                    if not (-90 <= latlng[0] <= 90) or not (-180 <= latlng[1] <= 180):
                        error_messages.append(f"Coordenadas fuera de rango para el país {country_data['name']['common']}")
                        continue

                    flag_png = country_data['flags'].get('png', '')
                    if not flag_png.startswith('http://') and not flag_png.startswith('https://'):
                        error_messages.append(f"URL de bandera no válida para el país {country_data['name']['common']}")
                        continue

                    if country_data['area'] <= 0:
                        error_messages.append(f"Área no válida para el país {country_data['name']['common']}")
                        continue

                    native_name = country_data['name'].get('nativeName', {})
                    native_name_eng = native_name.get('eng', {})
                    native_name_common = native_name_eng.get('common', '')

                    timezones = country_data.get('timezones', [])
                    if not timezones or not all(isinstance(tz, str) for tz in timezones):
                        error_messages.append(f"Timezones no válidos para el país {country_data['name']['common']}")
                        continue

                    continents = country_data.get('continents', [])
                    if not continents or not all(isinstance(cont, str) for cont in continents):
                        error_messages.append(f"Continentes no válidos para el país {country_data['name']['common']}")
                        continue

                    country, created = Country.objects.get_or_create(
                        common_name=country_data['name']['common'],
                        official_name=country_data['name']['official'],
                        native_name_common=native_name_common,
                        native_name_official=native_name_eng.get('official', ''),
                        capital=capital[0] if capital else '',
                        latitude=latlng[0] if len(latlng) > 0 else None,
                        longitude=latlng[1] if len(latlng) > 1 else None,
                        area=country_data['area'],
                        population=country_data['population'],
                        timezones=', '.join(timezones),
                        continents=', '.join(continents),
                        flag_png=flag_png,
                        flag_svg=country_data['flags'].get('svg', ''),
                    )

                    if created:
                        print(f"País {country_data['name']['common']} guardado correctamente.")
                    else:
                        print(f"País {country_data['name']['common']} ya existe.")

                transaction.on_commit(lambda: transaction.get_connection().cursor().execute("SELECT pg_advisory_unlock(123456)"))

                if not error_messages:
                    return {"message": "Países guardados correctamente."}

                return {"errors": "\n".join(error_messages)}

        except requests.RequestException as e:
            if attempt == retries - 1:
                print ("Sin respuesta")
            else:
                sleep(retry_delay)
                continue