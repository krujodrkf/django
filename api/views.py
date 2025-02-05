import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Country

class CountryList(APIView):
    """
    Vista que obtiene la lista de países desde el endpoint externo
    https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng
    Y guarda los datos en la base de datos sin duplicados y validando los datos.
    """
    def get(self, request, format=None):
        url = "https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng"
        error_messages = []  # Lista para almacenar mensajes de error

        try:
            # Realizar la solicitud GET al endpoint externo
            respuesta = requests.get(url)
            respuesta.raise_for_status()  # Levanta una excepción si el status no es 200 OK
            
            # Obtener los datos en formato JSON
            data = respuesta.json()
            
            # Guardar los países en la base de datos
            for country_data in data:
                # Validación de campos obligatorios
                if not country_data.get('name') or not country_data['name'].get('common'):
                    error_messages.append(f"Faltan datos para el país {country_data.get('name', {}).get('common', 'desconocido')}")
                    continue  # O lanzar un error

                # Validación de la capital
                capital = country_data.get('capital')
                if capital and not isinstance(capital[0], str):
                    error_messages.append(f"Capital no válida para el país {country_data['name']['common']}")
                    continue
                
                # Validación de población
                if not isinstance(country_data.get('population', 0), int):
                    error_messages.append(f"Población no válida para el país {country_data['name']['common']}")
                    continue
                                
                # Validación de coordenadas
                latlng = country_data.get('latlng', [])
                if len(latlng) != 2 or not all(isinstance(coord, (float, int)) for coord in latlng):
                    error_messages.append(f"Coordenadas no válidas para el país {country_data['name']['common']}")
                    continue
                # Validar que las coordenadas están dentro de los rangos lógicos
                if not (-90 <= latlng[0] <= 90) or not (-180 <= latlng[1] <= 180):
                    error_messages.append(f"Coordenadas fuera de rango para el país {country_data['name']['common']}")
                    continue
                
                # Validar URL de la bandera
                flag_png = country_data['flags'].get('png', '')
                if not flag_png.startswith('http://') and not flag_png.startswith('https://'):
                    error_messages.append(f"URL de bandera no válida para el país {country_data['name']['common']}")
                    continue  # O lanzar un error

                # Validación de área
                if country_data['area'] <= 0:
                    error_messages.append(f"Área no válida para el país {country_data['name']['common']}")
                    continue

                # Verificar que el país tenga un nombre nativo válido
                native_name = country_data['name'].get('nativeName', {})
                native_name_eng = native_name.get('eng', {})
                native_name_common = native_name_eng.get('common', '')

                # Validación de timezones y continentes
                timezones = country_data.get('timezones', [])
                if not timezones or not all(isinstance(tz, str) for tz in timezones):
                    error_messages.append(f"Timezones no válidos para el país {country_data['name']['common']}")
                    continue
                
                continents = country_data.get('continents', [])
                if not continents or not all(isinstance(cont, str) for cont in continents):
                    error_messages.append(f"Continentes no válidos para el país {country_data['name']['common']}")
                    continue
                
                # Verificar si el país ya existe en la base de datos
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
            
            # Si hay errores, devolvemos una respuesta con los mensajes
            if error_messages:
                return Response({"errors": "\n".join(error_messages)}, status=status.HTTP_400_BAD_REQUEST)
            
            # Devolver una respuesta exitosa si no hay errores
            return Response({"message": "Países guardados correctamente."}, status=status.HTTP_200_OK)
        
        except requests.RequestException as e:
            # En caso de error en la solicitud al endpoint
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
