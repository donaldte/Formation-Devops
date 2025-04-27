# app/urls.py
from django.urls import path
from .views import server_identity

urlpatterns = [
    path('', server_identity),  # page d'accueil
]
