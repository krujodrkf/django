import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import Country

class CountryList(APIView):
    """
    Vista que obtiene la lista de países desde el endpoint externo
    https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng
    Y guarda los datos en la base de datos sin duplicados.
    """
    def get(self, request, format=None):
        url = "https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng"
        
        try:
            # Realizar la solicitud GET al endpoint externo
            respuesta = requests.get(url)
            respuesta.raise_for_status()  # Levanta una excepción si el status no es 200 OK
            
            # Obtener los datos en formato JSON
            data = respuesta.json()
            
            # Guardar los países en la base de datos
            for country_data in data:
                # Extraer información de cada país
                native_name = country_data['name'].get('nativeName', {})
                native_name_eng = native_name.get('eng', {})
                
                # Verificar si el país ya existe en la base de datos
                country, created = Country.objects.get_or_create(
                    common_name=country_data['name']['common'],
                    official_name=country_data['name']['official'],
                    native_name_common=native_name_eng.get('common', ''),
                    native_name_official=native_name_eng.get('official', ''),
                    capital=country_data['capital'][0] if country_data.get('capital') else '',
                    latitude=country_data['latlng'][0] if len(country_data.get('latlng', [])) > 0 else None,
                    longitude=country_data['latlng'][1] if len(country_data.get('latlng', [])) > 1 else None,
                    area=country_data['area'],
                    population=country_data['population'],
                    timezones=', '.join(country_data['timezones']),
                    continents=', '.join(country_data['continents']),
                    flag_png=country_data['flags']['png'],
                    flag_svg=country_data['flags']['svg'],
                )
                
                # Si el país ya existe, `created` será False, de lo contrario, será True
                if created:
                    print(f"País {country_data['name']['common']} guardado correctamente.")
                else:
                    print(f"País {country_data['name']['common']} ya existe.")
            
            # Devolver una respuesta exitosa
            return Response({"message": "Países guardados correctamente."}, status=status.HTTP_200_OK)
        
        except requests.RequestException as e:
            # En caso de error en la solicitud al endpoint
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
