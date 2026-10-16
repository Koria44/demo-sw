"""
Encabezado: Panel de administración para apps/orders en demo-sw.
Permite inspeccionar pedidos generados, datos de contacto, dirección de entrega en Chile,
ítems comprados y actualizar el estado logístico del despacho.
"""
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Visualización inline de los productos que componen una orden."""
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'size', 'color_name', 'price_clp', 'quantity', 'line_total_clp')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Administración y seguimiento de pedidos de la tienda."""
    list_display = (
        'order_number',
        'full_name',
        'email',
        'phone',
        'region',
        'comuna',
        'formatted_total',
        'payment_method',
        'status',
        'created_at'
    )
    list_filter = ('status', 'region', 'payment_method', 'created_at')
    list_editable = ('status',)
    search_fields = ('order_number', 'first_name', 'last_name', 'email', 'rut', 'comuna')
    readonly_fields = ('order_number', 'subtotal_clp', 'shipping_cost_clp', 'total_clp', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
