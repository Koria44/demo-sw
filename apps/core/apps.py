"""
Encabezado: Configuración de la aplicación principal Core para demo-sw.
Centraliza la página de inicio, páginas estáticas informativas (Conócenos, Políticas, Contacto)
y procesadores de contexto globales de la tienda.
"""
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Núcleo del Sitio'
