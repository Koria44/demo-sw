"""
Encabezado: Enrutador URL principal para demo-sw (E-commerce NORTE Studio).
Conecta las aplicaciones modulares: core, catalog, cart, orders y newsletter,
así como el sitemap XML para indexación SEO y manejadores de error 404/500.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import StaticViewSitemap, CategorySitemap, CollectionSitemap, ProductSitemap

# Registro de sitemaps para el endpoint sitemap.xml
sitemaps = {
    'estaticas': StaticViewSitemap,
    'categorias': CategorySitemap,
    'colecciones': CollectionSitemap,
    'productos': ProductSitemap,
}

urlpatterns = [
    # Panel de control administrativo
    path('admin/', admin.site.urls),

    # Mapa del sitio XML para SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Carrito de compras (sesión y API del drawer)
    path('carrito/', include('apps.cart.urls', namespace='cart')),

    # Pedidos y checkout simulado
    path('pedidos/', include('apps.orders.urls', namespace='orders')),

    # Catálogo de prendas, categorías, búsqueda y reseñas
    path('catalogo/', include('apps.catalog.urls', namespace='catalog')),

    # Suscripción al boletín
    path('newsletter/', include('apps.newsletter.urls', namespace='newsletter')),

    # Núcleo del sitio (Home, Conócenos, Políticas, Contacto, robots.txt)
    path('', include('apps.core.urls', namespace='core')),
]

# Servir archivos multimedia (fotos subidas por el admin) en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Manejadores de error HTTP personalizados
handler404 = 'apps.core.views.custom_404_view'
handler500 = 'apps.core.views.custom_500_view'
