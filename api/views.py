import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from time import sleep
from .models import Country
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .serializers import CountrySerializer
from rest_framework.permissions import AllowAny
from rest_framework import filters

class CountryListView(ListAPIView):
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        country_id = self.kwargs.get('id') 
        if country_id:
            return Country.objects.filter(id=country_id)
        else:
            return Country.objects.all()
        

class CountryDetailView(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    lookup_field = 'id' 