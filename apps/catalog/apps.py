"""
Encabezado: Configuración de la aplicación de catálogo para demo-sw.
Gestiona categorías, colecciones, productos streetwear, variantes de color, tallas, stock y reseñas.
"""
from django.apps import AppConfig

class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.catalog'
    verbose_name = 'Catálogo de Ropa'
