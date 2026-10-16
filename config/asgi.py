"""
Encabezado: Punto de entrada ASGI para servidores asíncronos compatibles.
Expone la aplicación ASGI invocable como una variable a nivel de módulo llamada ``application``.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_asgi_application()
