"""
Encabezado: Configuración para el entorno de producción en demo-sw.
Aplica directivas estrictas de seguridad (HTTPS, cookies seguras, cabeceras HSTS),
desactiva DEBUG y requiere que SECRET_KEY y ALLOWED_HOSTS provengan de variables de entorno.
"""
from .base import *

DEBUG = False

# Verificación de clave secreta segura
if SECRET_KEY == 'django-insecure-demo-sw-streetwear-chile-key-2026-very-secret':
    raise ValueError("¡PELIGRO! Debes definir una SECRET_KEY segura en variables de entorno para producción.")

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

# Forzar redirección HTTPS si está detrás de un reverse proxy (como Nginx o Caddy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
