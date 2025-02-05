from django.urls import path
from .views import CountryList

urlpatterns = [
    path('countries/', CountryList.as_view(), name='country-list'),
]
