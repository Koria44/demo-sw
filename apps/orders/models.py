"""
Encabezado: Modelos de datos para pedidos y checkout en demo-sw (NORTE Studio).
Registra las órdenes generadas, los datos de despacho en Chile (RUT, Región, Comuna),
el desglose de ítems comprados y el estado del pedido.
"""
import uuid
from django.db import models
from apps.catalog.models import Product


class Order(models.Model):
    """
    Representa una orden de compra generada por un cliente en la tienda.
    Contiene la información de contacto, dirección de entrega en Chile y totales en CLP.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente de Pago'),
        ('confirmed', 'Confirmado y En Preparación'),
        ('shipped', 'Enviado con Número de Seguimiento'),
        ('delivered', 'Entregado al Cliente'),
        ('cancelled', 'Cancelado'),
    ]

    PAYMENT_CHOICES = [
        ('webpay', 'Webpay Plus (Débito / Crédito)'),
        ('transferencia', 'Transferencia Bancaria Directa'),
        ('mercadopago', 'Mercado Pago'),
    ]

    REGION_CHOICES = [
        ('RM', 'Región Metropolitana de Santiago'),
        ('VALPO', 'Región de Valparaíso'),
        ('BIOBIO', 'Región del Biobío'),
        ('ANTOF', 'Región de Antofagasta'),
        ('COQUIMBO', 'Región de Coquimbo'),
        ('OHIGGINS', "Región de O'Higgins"),
        ('MAULE', 'Región del Maule'),
        ('NUBLE', 'Región de Ñuble'),
        ('ARAUCANIA', 'Región de La Araucanía'),
        ('LOS_RIOS', 'Región de Los Ríos'),
        ('LOS_LAGOS', 'Región de Los Lagos'),
        ('ARICA', 'Región de Arica y Parinacota'),
        ('TARAPACA', 'Región de Tarapacá'),
        ('ATACAMA', 'Región de Atacama'),
        ('AYSEN', 'Región de Aysén'),
        ('MAGALLANES', 'Región de Magallanes'),
    ]

    order_number = models.CharField(
        max_length=32,
        unique=True,
        editable=False,
        verbose_name='Número de Pedido',
        help_text='Identificador único legible, ej: NSW-2026-9A4B'
    )
    # Datos personales del cliente
    first_name = models.CharField(max_length=60, verbose_name='Nombres')
    last_name = models.CharField(max_length=60, verbose_name='Apellidos')
    email = models.EmailField(verbose_name='Correo Electrónico')
    phone = models.CharField(max_length=20, verbose_name='Teléfono / Celular')
    rut = models.CharField(
        max_length=15,
        verbose_name='RUT del titular',
        help_text='Formato: 12.345.678-9 o 12345678-9'
    )

    # Datos de Despacho en Chile
    region = models.CharField(max_length=50, choices=REGION_CHOICES, verbose_name='Región de Despacho')
    comuna = models.CharField(
        max_length=80,
        verbose_name='Comuna',
        help_text='Ej: Providencia, Santiago Centro, Viña del Mar, Concepción'
    )
    address_line = models.CharField(max_length=200, verbose_name='Calle y Número')
    apartment_or_office = models.CharField(
        max_length=80,
        blank=True,
        verbose_name='Depto / Casa / Oficina (Opcional)'
    )
    delivery_notes = models.TextField(
        blank=True,
        verbose_name='Instrucciones para el repartidor (Opcional)'
    )

    # Montos y totales en CLP
    subtotal_clp = models.PositiveIntegerField(verbose_name='Subtotal Prendas (CLP)')
    shipping_cost_clp = models.PositiveIntegerField(
        default=0,
        verbose_name='Costo de Despacho (CLP)'
    )
    total_clp = models.PositiveIntegerField(verbose_name='Total Cancelado (CLP)')

    # Estado y pago
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_CHOICES,
        default='webpay',
        verbose_name='Método de Pago'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='confirmed',
        verbose_name='Estado del Pedido'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Emisión')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Pedido {self.order_number} - {self.full_name} (${self.formatted_total})"

    @property
    def full_name(self) -> str:
        """Nombre y apellido completo del destinatario."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def formatted_subtotal(self) -> str:
        return f"${self.subtotal_clp:,}".replace(',', '.')

    @property
    def formatted_shipping(self) -> str:
        if self.shipping_cost_clp == 0:
            return "GRATIS"
        return f"${self.shipping_cost_clp:,}".replace(',', '.')

    @property
    def formatted_total(self) -> str:
        return f"${self.total_clp:,}".replace(',', '.')

    def save(self, *args, **kwargs):
        """Genera un número de pedido único y legible antes de guardar si aún no existe."""
        if not self.order_number:
            code = uuid.uuid4().hex[:6].upper()
            self.order_number = f"NSW-2026-{code}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    Ítem individual de prenda dentro de un pedido consolidado.
    Preserva el estado y precio histórico al momento exacto de la compra.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Pedido Asociado'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items',
        verbose_name='Producto de Catálogo'
    )
    product_name = models.CharField(max_length=150, verbose_name='Nombre de la Prenda')
    size = models.CharField(max_length=10, verbose_name='Talla')
    color_name = models.CharField(max_length=50, verbose_name='Color')
    color_hex = models.CharField(max_length=7, default='#161616', verbose_name='Color Hex')
    garment_type = models.CharField(max_length=20, default='hoodie', verbose_name='Tipo de Prenda')
    price_clp = models.PositiveIntegerField(verbose_name='Precio Unitario (CLP)')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    line_total_clp = models.PositiveIntegerField(verbose_name='Total Línea (CLP)')

    class Meta:
        verbose_name = 'Ítem de Pedido'
        verbose_name_plural = 'Ítems de Pedidos'

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product_name} ({self.size}) - {self.order.order_number}"

    @property
    def formatted_price(self) -> str:
        return f"${self.price_clp:,}".replace(',', '.')

    @property
    def formatted_line_total(self) -> str:
        return f"${self.line_total_clp:,}".replace(',', '.')
