"""
Encabezado: Definición de Sitemaps XML para demo-sw (NORTE Studio).
Indexa las páginas estáticas, categorías, colecciones y productos disponibles para motores de búsqueda.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.catalog.models import Category, Collection, Product


class StaticViewSitemap(Sitemap):
    """Sitemap para páginas institucionales clave."""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'core:about', 'core:policies', 'core:contact', 'catalog:product_list', 'catalog:reviews_list']

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):
    """Sitemap para categorías activas del catálogo."""
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return Category.objects.filter(is_active=True)


class CollectionSitemap(Sitemap):
    """Sitemap para colecciones y drops activos."""
    priority = 0.85
    changefreq = 'weekly'

    def items(self):
        return Collection.objects.filter(is_active=True)


class ProductSitemap(Sitemap):
    """Sitemap para todas las prendas disponibles para compra."""
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at
