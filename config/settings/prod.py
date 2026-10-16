"""
Encabezado: Configuración para el entorno de producción en demo-sw (Render / Cloud).
Aplica directivas de seguridad para HTTPS, cookies seguras, integración automática con
dominios de Render (*.onrender.com), cabeceras HSTS y CSRF_TRUSTED_ORIGINS.
"""
import os
from .base import *

DEBUG = False

# Clave secreta: se recomienda definirla en el panel de Render
SECRET_KEY = env('SECRET_KEY', default='django-insecure-prod-demo-sw-render-key-2026-very-secret')

# Hosts permitidos: incluye por defecto subdominios de Render
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['.onrender.com', 'localhost', '127.0.0.1'])

# Soporte automático para el hostname dinámico asignado por Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Orígenes confiables para CSRF en peticiones POST (necesario en Django 4/5 bajo HTTPS)
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['https://*.onrender.com'])
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# Configuración de cookies seguras a través de HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Cabeceras de seguridad HTTP
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Encabezado proxy para detectar HTTPS en Render
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
