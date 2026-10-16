"""
Encabezado: Configuración para el entorno de desarrollo local en demo-sw.
Habilita el modo de depuración interactivo (DEBUG = True), almacenamiento estático no estricto
para facilitar iteración rápida con Tailwind CLI, y logging claro en consola.
"""
from .base import *

# Modo depuración activo para desarrollo
DEBUG = True

# Permitir todos los hosts locales
ALLOWED_HOSTS = ['*']

# En desarrollo utilizamos almacenamiento estático estándar para permitir cambios al vuelo en CSS/JS
# sin requerir ejecutar collectstatic cada vez que Tailwind recompile.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Backend de correo en consola para pruebas de confirmación de órdenes y newsletter
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
