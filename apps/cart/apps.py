"""
Encabezado: Configuración de la aplicación de carrito de compras para demo-sw.
Maneja el estado del carrito en la sesión del visitante sin requerir inicio de sesión previo.
"""
from django.apps import AppConfig

class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cart'
    verbose_name = 'Carrito de Compras'
