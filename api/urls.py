from django.urls import path
from .views import CountryListView, CountryDetailView

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country-list'),  # Lista de países
     path('countries/<int:id>/', CountryListView.as_view(), name='country-list-by-id'), 
]
