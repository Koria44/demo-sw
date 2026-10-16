"""
Encabezado: Configuración de la aplicación de Newsletter para demo-sw.
Gestiona las suscripciones al boletín por correo y la entrega de códigos de descuento de bienvenida.
"""
from django.apps import AppConfig

class NewsletterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.newsletter'
    verbose_name = 'Suscripciones y Newsletter'
