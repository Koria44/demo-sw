"""
Encabezado: Procesador de contexto global para demo-sw (NORTE Studio).
Inyecta en todas las plantillas los datos de la marca, umbral de envío gratis,
categorías y colecciones para el menú de navegación y pie de página con manejo seguro de excepciones.
"""
from django.conf import settings
from apps.catalog.models import Category, Collection


def store_context(request):
    """
    Expone variables globales de negocio y navegación a todas las plantillas.

    Args:
        request: HttpRequest actual.

    Returns:
        dict: Parámetros de marca y listados de categorías activas para el header.
    """
    try:
        categories = list(Category.objects.filter(is_active=True).order_by('order', 'name'))
        collections = list(Collection.objects.filter(is_active=True).order_by('-created_at'))
    except Exception:
        # En caso de que la base de datos se esté inicializando o migrando
        categories = []
        collections = []

    return {
        'STORE_BRAND_NAME': getattr(settings, 'STORE_BRAND_NAME', 'NORTE Studio'),
        'STORE_CONTACT_EMAIL': getattr(settings, 'STORE_CONTACT_EMAIL', 'contacto@nortestudio.cl'),
        'STORE_CONTACT_PHONE': getattr(settings, 'STORE_CONTACT_PHONE', '+56 9 8765 4321'),
        'FREE_SHIPPING_THRESHOLD': getattr(settings, 'FREE_SHIPPING_THRESHOLD', 70000),
        'nav_categories': categories,
        'nav_collections': collections,
    }
