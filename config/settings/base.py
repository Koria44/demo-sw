"""
Encabezado: Configuración base compartida del proyecto demo-sw (NORTE Studio).
Contiene los parámetros comunes a todos los entornos (desarrollo, testing y producción):
aplicaciones instaladas, middlewares, base de datos SQLite por defecto, internacionalización para Chile (es-cl, America/Santiago),
procesadores de contexto para la tienda e-commerce y configuración de archivos estáticos.
"""
from pathlib import Path
import environ

# Directorio raíz del proyecto: demo-sw/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Compatibilidad para pruebas en Python 3.14 (corrección de copia de BaseContext)
from django.template import context as django_context
def _base_context_copy(self):
    duplicate = self.__class__.__new__(self.__class__)
    duplicate.dicts = self.dicts[:]
    return duplicate
django_context.BaseContext.__copy__ = _base_context_copy

# Inicialización de django-environ para lectura de variables de entorno
env = environ.Env(
    DEBUG=(bool, False),
    FREE_SHIPPING_THRESHOLD=(int, 70000),
    STANDARD_SHIPPING_COST=(int, 3990),
)

# Carga de archivo .env si existe en la raíz
env_file = BASE_DIR / '.env'
if env_file.exists():
    environ.Env.read_env(str(env_file))

# Clave secreta (sobrescribir en producción mediante variable de entorno)
SECRET_KEY = env('SECRET_KEY', default='django-insecure-demo-sw-streetwear-chile-key-2026-very-secret')

# Control de depuración (False por defecto en base, True en dev.py)
DEBUG = env.bool('DEBUG', default=False)

# Hosts permitidos
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', '0.0.0.0'])

# Definición de aplicaciones instaladas
INSTALLED_APPS = [
    # Aplicaciones nativas de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # Aplicaciones del proyecto demo-sw
    'apps.core.apps.CoreConfig',
    'apps.catalog.apps.CatalogConfig',
    'apps.cart.apps.CartConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.newsletter.apps.NewsletterConfig',
]

# Pipeline de Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise permite servir archivos estáticos con compresión gzip/brotli y caché
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Configuración del motor de plantillas de Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Procesadores estándar de Django
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Procesador de contexto global para la tienda streetwear NORTE Studio
                'apps.core.context_processors.store_context',
                # Procesador de contexto para exponer el estado actual del carrito
                'apps.cart.context_processors.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Configuración de base de datos
# Utiliza SQLite por defecto para la demo local o URL de base de datos si se provee
DATABASES = {
    'default': env.db('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

# Validadores de contraseñas de usuario
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización y Localización (Chile)
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JavaScript, imágenes vectoriales)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración de compresión y caché de WhiteNoise (robusto sin fallos por manifest estricto)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Archivos subidos por usuarios (imágenes de producto reales opcionales)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Identificador de sesión para almacenar el carrito de compras anónimo
CART_SESSION_ID = 'sw_cart'

# Clave primaria por defecto para modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# Parámetros de Negocio de la Marca (NORTE Studio)
# ==============================================================================
STORE_BRAND_NAME = env('STORE_BRAND_NAME', default='NORTE Studio')
STORE_CONTACT_EMAIL = env('STORE_CONTACT_EMAIL', default='contacto@nortestudio.cl')
STORE_CONTACT_PHONE = env('STORE_CONTACT_PHONE', default='+56 9 8765 4321')

# Envío gratuito para compras sobre $70.000 CLP
FREE_SHIPPING_THRESHOLD = env.int('FREE_SHIPPING_THRESHOLD', default=70000)
# Costo de envío estándar en CLP para órdenes bajo el umbral gratuito
STANDARD_SHIPPING_COST = env.int('STANDARD_SHIPPING_COST', default=3990)
