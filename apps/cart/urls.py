"""
Encabezado: Rutas URL para la aplicación de Carrito de Compras en demo-sw.
Define endpoints para agregar, modificar cantidad, eliminar productos y consultar el estado en JSON.
"""
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Vista de página completa del carrito
    path('', views.cart_detail, name='cart_detail'),
    path('vaciar/', views.cart_clear, name='cart_clear'),

    # Endpoints JSON para el drawer interactivo
    path('api/agregar/', views.cart_add, name='cart_add'),
    path('api/actualizar/', views.cart_update, name='cart_update'),
    path('api/eliminar/', views.cart_remove, name='cart_remove'),
    path('api/estado/', views.cart_state_api, name='cart_state_api'),
]
