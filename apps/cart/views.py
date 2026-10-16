"""
Encabezado: Vistas y endpoints de la API del Carrito de Compras para demo-sw.
Ofrece endpoints JSON con soporte para peticiones fetch/AJAX desde el drawer interactivo
y vistas estándar para fallback sin JavaScript.
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from apps.catalog.models import Product, ProductColor, ProductSize
from .cart import Cart


@require_POST
def cart_add(request):
    """
    Endpoint para agregar una prenda al carrito.
    Exige la selección explícita de talla antes de procesar.
    Soporta JSON body o Form-data.
    """
    cart = Cart(request)

    # Detección de payload JSON o formulario estándar
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    else:
        data = request.POST

    product_id = data.get('product_id')
    size = data.get('size', '').strip().upper()
    color_id = data.get('color_id')
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return JsonResponse({'error': 'ID de producto no proporcionado'}, status=400)

    # Validación estricta de selección de talla
    if not size:
        return JsonResponse({
            'error': 'Debes seleccionar una talla antes de agregar la prenda al carrito.',
            'field': 'size'
        }, status=422)

    product = get_object_or_404(Product, id=product_id, is_active=True)

    # Validación de existencia de talla y stock
    size_obj = ProductSize.objects.filter(product=product, size=size, is_active=True).first()
    if not size_obj or size_obj.stock <= 0:
        return JsonResponse({
            'error': f'La talla {size} se encuentra agotada en este momento.',
            'field': 'size'
        }, status=422)

    # Validación o fallback de color
    if color_id:
        color = ProductColor.objects.filter(id=color_id, product=product).first()
    else:
        color = product.default_color

    resolved_color_id = color.id if color else 0

    # Agregar al carrito
    item = cart.add(
        product=product,
        size=size,
        color_id=resolved_color_id,
        quantity=quantity
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'message': f'"{product.name}" (Talla {size}) agregado al carrito.',
            'item': item,
            'cart': cart.to_dict()
        })

    messages.success(request, f'"{product.name}" fue agregado a tu carrito.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request):
    """
    Endpoint para modificar la cantidad de unidades de un ítem en el carrito.
    """
    cart = Cart(request)

    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    else:
        data = request.POST

    item_key = data.get('item_key')
    quantity = int(data.get('quantity', 1))

    if not item_key:
        return JsonResponse({'error': 'Clave de ítem requerida'}, status=400)

    cart.update_quantity(item_key=item_key, quantity=quantity)

    return JsonResponse({
        'success': True,
        'cart': cart.to_dict()
    })


@require_POST
def cart_remove(request):
    """
    Endpoint para eliminar una prenda específica del carrito.
    """
    cart = Cart(request)

    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    else:
        data = request.POST

    item_key = data.get('item_key')
    if not item_key:
        return JsonResponse({'error': 'Clave de ítem requerida'}, status=400)

    cart.remove(item_key)

    return JsonResponse({
        'success': True,
        'message': 'Prenda eliminada del carrito.',
        'cart': cart.to_dict()
    })


@require_GET
def cart_state_api(request):
    """
    Endpoint para sincronizar el estado del carrito en el cliente al cargar la página.
    """
    cart = Cart(request)
    return JsonResponse(cart.to_dict())


def cart_detail(request):
    """
    Vista de página completa del carrito de compras (alternativa al drawer lateral).
    """
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {
        'cart': cart
    })


def cart_clear(request):
    """
    Vacía todo el carrito de la sesión.
    """
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'El carrito ha sido vaciado.')
    return redirect('cart:cart_detail')
