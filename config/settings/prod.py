"""
Encabezado: Configuración para el entorno de producción en demo-sw (Render / Cloud).
Aplica directivas de seguridad para HTTPS, cookies seguras, integración automática con
dominios de Render (*.onrender.com), cabeceras HSTS y CSRF_TRUSTED_ORIGINS.
"""
import os
from .base import *

DEBUG = env.bool('DEBUG', default=False)

# Clave secreta: se recomienda definirla en el panel de Render
SECRET_KEY = env('SECRET_KEY', default='django-insecure-prod-demo-sw-render-key-2026-very-secret')

# Hosts permitidos: permitimos todos los subdominios de Render y hosts locales
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# Soporte automático para el hostname dinámico asignado por Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

# Orígenes confiables para CSRF en peticiones POST (necesario en Django 4/5 bajo HTTPS)
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[
    'https://*.onrender.com',
    'https://demo-sw.onrender.com'
])
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# Configuración de cookies seguras a través de HTTPS
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)

# Cabeceras de seguridad HTTP
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Encabezado proxy para detectar HTTPS en Render
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Render maneja SSL automáticamente en el borde; evitamos redirecciones en bucle
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
