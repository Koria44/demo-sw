"""
Encabezado: Configuración de la aplicación de pedidos y checkout para demo-sw.
Gestiona el proceso de compra simulado con despacho a regiones y comunas de Chile.
"""
from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'
    verbose_name = 'Órdenes y Pedidos'
