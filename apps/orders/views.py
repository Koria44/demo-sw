"""
Encabezado: Vistas para el flujo de Checkout y Confirmación de Pedido en demo-sw.
Valida el carro activo, registra la orden en base de datos, descuenta el stock de las tallas compradas,
vacía el carrito de compras y presenta una pantalla de confirmación con número de seguimiento.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.cart.cart import Cart
from apps.catalog.models import Product, ProductSize
from .models import Order, OrderItem
from .forms import CheckoutForm


def checkout_view(request):
    """
    Vista de checkout y despacho.
    Si el carrito está vacío, redirige al catálogo.
    En método POST, procesa los datos del cliente, persiste la orden y sus ítems,
    actualiza el stock disponible y limpia la sesión del carrito.
    """
    cart = Cart(request)

    # Si no hay ítems en el carrito, no se puede iniciar el checkout
    if cart.total_items == 0:
        messages.warning(request, 'Tu carrito de compras está vacío. Agrega prendas para continuar.')
        return redirect('catalog:product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # Asignamos los montos consolidados calculados por el motor del carrito
            order.subtotal_clp = cart.subtotal_clp
            order.shipping_cost_clp = cart.standard_shipping_cost
            order.total_clp = cart.total_clp
            order.save()

            # Creación de ítems de la orden y descuento de inventario
            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=item['name'],
                    size=item['size'],
                    color_name=item['color_name'],
                    color_hex=item['color_hex'],
                    garment_type=item['garment_type'],
                    price_clp=item['price_clp'],
                    quantity=item['quantity'],
                    line_total_clp=item['line_total_clp'],
                )

                # Descuento atómico de stock por talla
                size_obj = ProductSize.objects.filter(product=product, size=item['size']).first()
                if size_obj and size_obj.stock >= item['quantity']:
                    size_obj.stock -= item['quantity']
                    size_obj.save()

            # Vaciar el carrito de la sesión
            cart.clear()

            # Guardamos el número de pedido en la sesión para acceso seguro a la pantalla de éxito
            request.session['last_order_number'] = order.order_number
            return redirect('orders:order_success', order_number=order.order_number)
        else:
            messages.error(request, 'Por favor revisa los campos marcados en rojo en el formulario.')
    else:
        form = CheckoutForm(initial={
            'payment_method': 'webpay',
            'region': 'RM',
        })

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
    })


def order_success_view(request, order_number):
    """
    Pantalla de confirmación de pedido y éxito de compra.
    Muestra el número de pedido, el resumen de prendas adquiridas,
    la dirección de despacho en Chile y los plazos estimados de entrega.
    """
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/order_success.html', {
        'order': order,
    })
