import requests #No se usa en este archivo
from rest_framework.views import APIView #Clases de Django Rest Framework para manejar vistas de APIs
from rest_framework.response import Response #Clases de Django Rest Framework para manejar respuestas de APIs
from rest_framework import status #Clases de Django Rest Framework para manejar códigos de estado de APIs
from time import sleep #Pausar ejecución de código
from .models import Country #Importar modelo de Country
from rest_framework.generics import ListAPIView,RetrieveAPIView #Clases de Django Rest Framework para manejar vistas de APIs
from .serializers import CountrySerializer #Importar serializador de Country
from rest_framework.permissions import AllowAny #Clases de Django Rest Framework para manejar permisos de APIs
from rest_framework import filters #Clases de Django Rest Framework para manejar filtros de APIs

class CountryListView(ListAPIView): #ListAPIView es una clase de Django Rest Framework que permite listar objetos de un modelo
    serializer_class = CountrySerializer #Convierte objetos de tipo Country a JSON
    permission_classes = [AllowAny] #Permite el acceso a cualquier usuario

    def get_queryset(self): #Método que retorna los objetos que se listarán	
        country_id = self.kwargs.get('id')  #Obtener el id del país de la URL	
        if country_id: #Si se especifica un id de país en la URL ESTÁ AL PEDO ya que ListAPIView no se usa para detalles sino para listas
            return Country.objects.filter(id=country_id) #  Retornar el país con ese id
        else: #Si no se especifica un id de país en la URL	
            return Country.objects.all() #Retornar todos los países	
        

class CountryDetailView(RetrieveAPIView): #RetrieveAPIView es una clase de Django Rest Framework que permite obtener un objeto de un modelo
    queryset = Country.objects.all() #Obtener todos los objetos de tipo Country
    serializer_class = CountrySerializer #Convierte objetos de tipo Country a JSON	
    permission_classes = [AllowAny] #Permite el acceso a cualquier usuario
    lookup_field = 'id' #Campo que se usará para buscar el objeto