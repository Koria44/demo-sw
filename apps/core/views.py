"""
Encabezado: Vistas estáticas y página de inicio para demo-sw (NORTE Studio).
Gestiona la portada con catálogo destacado, páginas corporativas (Conócenos, Políticas, Contacto)
y respuestas de infraestructura SEO (robots.txt y errores 404/500 personalizados).
"""
from django.shortcuts import render
from django.http import HttpResponse
from apps.catalog.models import Product, Category, Collection, Review


def home_view(request):
    """
    Vista principal (Home) de la tienda streetwear.
    Carga el hero editorial, las categorías para las tarjetas lookbook,
    las prendas destacadas con prefetch optimizado y las reseñas más recientes.
    """
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('category').prefetch_related('colors', 'sizes')[:8]

    new_arrivals = Product.objects.filter(
        is_active=True,
        is_new=True
    ).select_related('category').prefetch_related('colors', 'sizes')[:8]

    # Cápsula o Drop principal
    main_drop = Collection.objects.filter(is_active=True).first()

    # Reseñas destacadas de 5 estrellas
    highlight_reviews = Review.objects.filter(
        rating=5
    ).select_related('product')[:6]

    return render(request, 'core/home.html', {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'main_drop': main_drop,
        'highlight_reviews': highlight_reviews,
    })


def about_view(request):
    """Vista 'Conócenos': manifiesto de confección, gramajes pesados y taller en Chile."""
    return render(request, 'core/about.html')


def policies_view(request):
    """Vista de 'Políticas de Despacho y Devoluciones' con detalles de logística nacional."""
    return render(request, 'core/policies.html')


def contact_view(request):
    """Vista de contacto y showroom en Santiago de Chile."""
    return render(request, 'core/contact.html')


def robots_txt_view(request):
    """
    Genera dinámicamente el archivo robots.txt para motores de búsqueda.
    Bloquea rutas privadas (carrito, checkout, búsqueda interna) y referencia el sitemap XML.
    """
    lines = [
        "User-agent: *",
        "Disallow: /carrito/",
        "Disallow: /checkout/",
        "Disallow: /buscar/",
        "Disallow: /admin/",
        "Disallow: /api/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def custom_404_view(request, exception=None):
    """Página 404 personalizada con enlaces amigables a categorías y catálogo."""
    return render(request, '404.html', status=404)


def custom_500_view(request):
    """Página 500 personalizada para errores internos del servidor."""
    return render(request, '500.html', status=500)
