"""
Encabezado: Pruebas unitarias para pedidos y checkout en apps/orders/tests.py.
Comprueba la validación de RUT chileno, generación de números de orden y checkout.
"""
from django.test import TestCase, Client
from django.urls import reverse
from apps.catalog.models import Category, Product, ProductSize
from apps.orders.forms import CheckoutForm
from apps.orders.models import Order


class OrdersTestCase(TestCase):
    """Pruebas del proceso de checkout y despacho en Chile."""

    def test_rut_validation(self):
        """Comprueba que el validador acepte RUTs válidos y rechace formatos incorrectos."""
        # RUT válido con puntos y guion
        form_valid = CheckoutForm(data={
            'first_name': 'Benjamín',
            'last_name': 'González',
            'email': 'benja@test.cl',
            'phone': '+56912345678',
            'rut': '12.345.678-9',
            'region': 'RM',
            'comuna': 'Providencia',
            'address_line': 'Av. Providencia 1234',
            'payment_method': 'webpay',
        })
        self.assertTrue(form_valid.is_valid(), form_valid.errors)

        # RUT inválido sin guion o caracteres aleatorios
        form_invalid = CheckoutForm(data={
            'first_name': 'Benjamín',
            'last_name': 'González',
            'email': 'benja@test.cl',
            'phone': '+56912345678',
            'rut': '12345', # demasiado corto
            'region': 'RM',
            'comuna': 'Providencia',
            'address_line': 'Av. Providencia 1234',
            'payment_method': 'webpay',
        })
        self.assertFalse(form_invalid.is_valid())
        self.assertIn('rut', form_invalid.errors)

    def test_order_number_auto_generation(self):
        """Verifica que el modelo Order genere automáticamente un identificador NSW-2026-XXXX."""
        order = Order.objects.create(
            first_name='Carlos',
            last_name='Silva',
            email='carlos@test.cl',
            phone='+56999887766',
            rut='18223344-5',
            region='VALPO',
            comuna='Viña del Mar',
            address_line='1 Norte 500',
            subtotal_clp=60000,
            shipping_cost_clp=3990,
            total_clp=63990,
            payment_method='webpay'
        )
        self.assertTrue(order.order_number.startswith('NSW-2026-'))
        self.assertEqual(order.formatted_total, '$63.990')
