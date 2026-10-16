"""
Encabezado: Pruebas unitarias para el Carrito de Compras en apps/cart/tests.py.
Valida la adición de prendas con talla obligatoria, cálculo de subtotales en CLP,
progreso de despacho gratuito ($70.000) y endpoints JSON.
"""
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from apps.catalog.models import Category, Product, ProductColor, ProductSize
from apps.cart.cart import Cart


class CartTestCase(TestCase):
    """Conjunto de pruebas para la lógica de negocio del carrito en sesión."""

    def setUp(self):
        """Prepara datos de prueba para productos, colores y tallas."""
        self.factory = RequestFactory()

        # Categoría
        self.category = Category.objects.create(
            name='Hoodies Test',
            slug='hoodies-test',
            garment_type='hoodie'
        )

        # Producto
        self.product = Product.objects.create(
            category=self.category,
            name='Hoodie Test 450 GSM',
            slug='hoodie-test-450-gsm',
            price_clp=50000,
            fabric_details='100% Algodón',
            garment_type='hoodie',
            is_active=True
        )

        # Color
        self.color = ProductColor.objects.create(
            product=self.product,
            name='Negro Carbón',
            hex_code='#161616',
            is_default=True
        )

        # Tallas
        self.size_m = ProductSize.objects.create(
            product=self.product,
            size='M',
            stock=10
        )

    def _get_request_with_session(self):
        """Genera una petición HTTP simulada con middleware de sesión activo."""
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        return request

    def test_cart_add_and_subtotal(self):
        """Verifica que al agregar una prenda se calcule el subtotal y cantidad correctamente."""
        request = self._get_request_with_session()
        cart = Cart(request)

        # Agregar 1 unidad de Hoodie ($50.000 CLP)
        cart.add(product=self.product, size='M', color_id=self.color.id, quantity=1)

        self.assertEqual(cart.total_items, 1)
        self.assertEqual(cart.subtotal_clp, 50000)
        self.assertFalse(cart.qualifies_for_free_shipping)
        # Faltan $20.000 para llegar a $70.000
        self.assertEqual(cart.remaining_for_free_shipping, 20000)

    def test_free_shipping_threshold(self):
        """Verifica que al superar $70.000 CLP se active el despacho gratuito."""
        request = self._get_request_with_session()
        cart = Cart(request)

        # Agregar 2 unidades ($100.000 CLP)
        cart.add(product=self.product, size='M', color_id=self.color.id, quantity=2)

        self.assertEqual(cart.subtotal_clp, 100000)
        self.assertTrue(cart.qualifies_for_free_shipping)
        self.assertEqual(cart.standard_shipping_cost, 0)
        self.assertEqual(cart.formatted_shipping_cost, "GRATIS")

    def test_cart_remove_item(self):
        """Verifica la eliminación de prendas del carrito."""
        request = self._get_request_with_session()
        cart = Cart(request)

        item = cart.add(product=self.product, size='M', color_id=self.color.id, quantity=1)
        item_key = f"{self.product.id}_M_{self.color.id}"

        self.assertEqual(cart.total_items, 1)
        cart.remove(item_key)
        self.assertEqual(cart.total_items, 0)
        self.assertEqual(cart.subtotal_clp, 0)
