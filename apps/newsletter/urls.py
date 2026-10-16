"""
Encabezado: Rutas URL para la aplicación de Newsletter en demo-sw.
Define el endpoint para el envío del formulario de suscripción.
"""
from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('suscribir/', views.subscribe_view, name='subscribe'),
]
