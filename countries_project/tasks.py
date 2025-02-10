from django.db import transaction
from time import sleep
import requests
from celery import shared_task
from api.models import Country

@shared_task
def update_country_data():
    """
    Función que obtiene la lista de países desde el endpoint externo
    y actualiza o inserta los datos en la base de datos.
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
                    common_name = country_data.get("name", {}).get("common")
                    official_name = country_data.get("name", {}).get("official", "")
                    if not common_name:
                        error_messages.append("Faltan datos del país.")
                        continue

                    capital = country_data.get("capital", [])
                    capital_name = capital[0] if capital and isinstance(capital[0], str) else ""

                    population = country_data.get("population", 0)
                    if not isinstance(population, int) or population < 0:
                        error_messages.append(f"Población no válida para {common_name}.")
                        continue

                    latlng = country_data.get("latlng", [])
                    latitude = latlng[0] if len(latlng) == 2 and isinstance(latlng[0], (float, int)) else None
                    longitude = latlng[1] if len(latlng) == 2 and isinstance(latlng[1], (float, int)) else None

                    area = country_data.get("area", 0)
                    if not isinstance(area, (float, int)) or area <= 0:
                        error_messages.append(f"Área no válida para {common_name}.")
                        continue

                    timezones = ", ".join(country_data.get("timezones", []))
                    continents = ", ".join(country_data.get("continents", []))

                    flags = country_data.get("flags", {})
                    flag_png = flags.get("png", "")
                    flag_svg = flags.get("svg", "")

                    native_name_data = country_data.get("name", {}).get("nativeName", {})
                    native_name_eng = native_name_data.get("eng", {})
                    native_name_common = native_name_eng.get("common", "")
                    native_name_official = native_name_eng.get("official", "")

                    
                    country, created = Country.objects.update_or_create(
                        common_name=common_name,
                        defaults={
                            "official_name": official_name,
                            "native_name_common": native_name_common,
                            "native_name_official": native_name_official,
                            "capital": capital_name,
                            "latitude": latitude,
                            "longitude": longitude,
                            "area": area,
                            "population": population,
                            "timezones": timezones,
                            "continents": continents,
                            "flag_png": flag_png,
                            "flag_svg": flag_svg,
                        }
                    )

                    if created:
                        print(f"✅ País agregado: {common_name}.")
                    else:
                        print(f"🔄 País actualizado: {common_name}.")

                transaction.on_commit(lambda: transaction.get_connection().cursor().execute("SELECT pg_advisory_unlock(123456)"))

                if not error_messages:
                    return {"message": "Países actualizados correctamente."}

                return {"errors": "\n".join(error_messages)}

        except requests.RequestException:
            if attempt == retries - 1:
                print("🚨 Error: No se pudo obtener la información de los países.")
            else:
                print(f"🔄 Reintentando en {retry_delay} segundos...")
                sleep(retry_delay)
                continue
