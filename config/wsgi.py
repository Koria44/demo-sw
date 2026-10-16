"""
Encabezado: Punto de entrada WSGI para servidores web compatibles.
Expone la aplicación WSGI invocable como una variable a nivel de módulo llamada ``application``.
"""
import os
from django.core.wsgi import get_wsgi_application

# Detecta automáticamente si está en Render o en producción
if os.environ.get('DJANGO_ENV') == 'production' or os.environ.get('RENDER'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_wsgi_application()
