"""
Encabezado: Rutas URL para el catálogo de productos de demo-sw (NORTE Studio).
Define endpoints con slugs limpios en español para navegación, filtrado, detalle de prendas,
búsqueda en vivo y testimonios.
"""
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Catálogo completo
    path('', views.ProductListView.as_view(), name='product_list'),

    # Listados filtrados por taxonomía
    path('categoria/<slug:category_slug>/', views.ProductListView.as_view(), name='category_detail'),
    path('coleccion/<slug:collection_slug>/', views.ProductListView.as_view(), name='collection_detail'),

    # Ficha técnica y detalle de prenda
    path('producto/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Búsqueda
    path('buscar/', views.SearchView.as_view(), name='search'),
    path('api/buscar/', views.ProductSearchJsonView.as_view(), name='search_api'),

    # Reseñas comunitarias
    path('resenas/', views.ReviewsListView.as_view(), name='reviews_list'),
]
