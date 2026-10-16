"""
Encabezado: Vistas de catálogo para demo-sw (NORTE Studio).
Gestiona el listado de prendas con filtros avanzados (categoría, colección, talla, color, precio),
ordenamiento, vista detallada del producto con selector de tallas y variantes,
búsqueda en vivo mediante endpoint JSON con debounce y página de reseñas de clientes.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, Collection, Product, ProductColor, ProductSize, Review


class ProductListView(ListView):
    """
    Vista de catálogo principal y filtrado de productos streetwear.
    Soporta filtros por categoría, colección, talla, familia de color y rango de precios,
    con paginación y optimización de consultas SQL (select_related y prefetch_related).
    """
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """
        Construye el conjunto de datos optimizado aplicando filtros dinámicos por URL y GET query params.
        """
        # Consulta base solo con productos activos y pre-carga de relaciones para evitar N+1 queries
        qs = Product.objects.filter(is_active=True).select_related(
            'category', 'collection'
        ).prefetch_related('colors', 'sizes', 'reviews')

        # Filtro por slug de categoría (desde la URL o query param)
        category_slug = self.kwargs.get('category_slug') or self.request.GET.get('categoria')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        # Filtro por slug de colección / drop
        collection_slug = self.kwargs.get('collection_slug') or self.request.GET.get('coleccion')
        if collection_slug:
            qs = qs.filter(collection__slug=collection_slug)

        # Filtro por talla (XS, S, M, L, XL, XXL)
        size_filter = self.request.GET.get('talla')
        if size_filter:
            qs = qs.filter(sizes__size=size_filter, sizes__stock__gt=0).distinct()

        # Filtro por familia de color (sw-black, sw-melange, etc.)
        color_filter = self.request.GET.get('color')
        if color_filter:
            qs = qs.filter(colors__color_family=color_filter).distinct()

        # Filtro por rango de precio en CLP
        min_price = self.request.GET.get('precio_min')
        if min_price and min_price.isdigit():
            qs = qs.filter(price_clp__gte=int(min_price))

        max_price = self.request.GET.get('precio_max')
        if max_price and max_price.isdigit():
            qs = qs.filter(price_clp__lte=int(max_price))

        # Criterio de ordenamiento
        order_by = self.request.GET.get('orden', 'recientes')
        if order_by == 'precio_asc':
            qs = qs.order_by('price_clp')
        elif order_by == 'precio_desc':
            qs = qs.order_by('-price_clp')
        elif order_by == 'populares':
            qs = qs.order_by('-is_featured', '-created_at')
        else: # 'recientes' por defecto
            qs = qs.order_by('-created_at')

        return qs

    def get_context_data(self, **kwargs):
        """Añade metadatos de filtros, categorías y colecciones al contexto de la plantilla."""
        context = super().get_context_data(**kwargs)

        # Categoría activa si aplica
        category_slug = self.kwargs.get('category_slug') or self.request.GET.get('categoria')
        current_category = None
        if category_slug:
            current_category = Category.objects.filter(slug=category_slug).first()

        # Colección activa si aplica
        collection_slug = self.kwargs.get('collection_slug') or self.request.GET.get('coleccion')
        current_collection = None
        if collection_slug:
            current_collection = Collection.objects.filter(slug=collection_slug).first()

        context.update({
            'current_category': current_category,
            'current_collection': current_collection,
            'categories': Category.objects.filter(is_active=True),
            'collections': Collection.objects.filter(is_active=True),
            'size_choices': ProductSize.SIZE_CHOICES,
            'color_choices': ProductColor.COLOR_FAMILY_CHOICES,
            'selected_size': self.request.GET.get('talla', ''),
            'selected_color': self.request.GET.get('color', ''),
            'selected_order': self.request.GET.get('orden', 'recientes'),
            'selected_min_price': self.request.GET.get('precio_min', ''),
            'selected_max_price': self.request.GET.get('precio_max', ''),
            'total_count': self.get_queryset().count(),
        })
        return context


class ProductDetailView(DetailView):
    """
    Vista detallada de una prenda streetwear.
    Presenta la galería/ilustración interactiva, selector de color que conmuta el SVG en vivo,
    selector de tallas con disponibilidad de stock, guía de tallas, detalles de confección
    y recomendaciones de productos relacionados.
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """Optimiza la consulta cargando de antemano colores, tallas y reseñas vinculadas."""
        return Product.objects.filter(is_active=True).select_related(
            'category', 'collection'
        ).prefetch_related('colors', 'sizes', 'reviews')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Recomendaciones de la misma categoría excluyendo el producto actual
        related_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id).select_related('category').prefetch_related('colors', 'sizes')[:4]

        # Reseñas del producto
        reviews = product.reviews.all()

        context.update({
            'related_products': related_products,
            'reviews': reviews,
            'default_color': product.default_color,
            'has_reviews': reviews.exists(),
        })
        return context


class ProductSearchJsonView(View):
    """
    Endpoint JSON para el overlay de búsqueda en vivo con debounce.
    Recibe el término 'q' y devuelve coincidencias de productos en formato JSON rápido.
    """
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        if len(query) < 2:
            return JsonResponse({'results': []})

        # Búsqueda insensible a mayúsculas/minúsculas en nombre, descripción y categoría
        matches = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(fabric_details__icontains=query),
            is_active=True
        ).select_related('category').prefetch_related('colors')[:8]

        results = []
        for p in matches:
            default_color = p.default_color
            results.append({
                'id': p.id,
                'name': p.name,
                'slug': p.slug,
                'url': p.get_absolute_url(),
                'category_name': p.category.name,
                'price_clp': p.price_clp,
                'formatted_price': p.formatted_price,
                'garment_type': p.garment_type,
                'hex_code': default_color.hex_code if default_color else '#161616',
                'has_image': bool(p.image),
                'image_url': p.image.url if p.image else '',
            })

        return JsonResponse({'results': results})


class SearchView(ListView):
    """
    Vista completa de resultados de búsqueda para usuarios que presionan Enter o no usan JS.
    """
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return Product.objects.none()

        return Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(fabric_details__icontains=query),
            is_active=True
        ).select_related('category', 'collection').prefetch_related('colors', 'sizes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        context.update({
            'search_query': query,
            'is_search_page': True,
            'total_count': self.get_queryset().count(),
        })
        return context


class ReviewsListView(ListView):
    """
    Vista editorial dedicada a las reseñas y testimonios de la comunidad de NORTE Studio.
    """
    model = Review
    template_name = 'catalog/reviews.html'
    context_object_name = 'reviews'
    paginate_by = 16

    def get_queryset(self):
        return Review.objects.select_related('product', 'product__category').order_by('-created_at')
