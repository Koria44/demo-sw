"""
Encabezado: Rutas URL para la aplicación de Checkout y Pedidos en demo-sw.
Define las rutas para el formulario de pago y la pantalla de orden exitosa.
"""
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirmacion/<str:order_number>/', views.order_success_view, name='order_success'),
]
