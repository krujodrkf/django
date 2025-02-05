from django.shortcuts import render

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CountryList(APIView):
    """
    Vista que obtiene la lista de países desde el endpoint externo
    https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng
    """
    def get(self, request, format=None):
        url = "https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng"
        try:
            respuesta = requests.get(url)
            respuesta.raise_for_status()  # Levanta una excepción si el status no es 200 OK
            data = respuesta.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

