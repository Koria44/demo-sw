"""
Encabezado: Punto de entrada WSGI para servidores web compatibles.
Expone la aplicación WSGI invocable como una variable a nivel de módulo llamada ``application``.
"""
import os
from django.core.wsgi import get_wsgi_application

# Carga la configuración base o la definida en el entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_wsgi_application()
