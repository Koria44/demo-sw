"""
Encabezado: Pruebas unitarias para el catálogo de productos en apps/catalog/tests.py.
Comprueba respuestas de vistas de listado, detalle, formato de precio chileno y endpoint JSON de búsqueda.
"""
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product, ProductColor, ProductSize, Review


class CatalogTestCase(TestCase):
    """Pruebas del módulo de catálogo y búsqueda."""

    def setUp(self):
        self.client = Client()

        self.category = Category.objects.create(
            name='Poleras Boxy',
            slug='poleras-boxy',
            garment_type='tee'
        )

        self.product = Product.objects.create(
            category=self.category,
            name='Polera Boxy 260 GSM',
            slug='polera-boxy-260-gsm',
            price_clp=29990,
            compare_price_clp=34990,
            fabric_details='100% Algodón',
            garment_type='tee',
            is_active=True
        )

        self.color = ProductColor.objects.create(
            product=self.product,
            name='Negro Carbón',
            hex_code='#161616',
            is_default=True
        )

        self.size = ProductSize.objects.create(
            product=self.product,
            size='L',
            stock=15
        )

    def test_product_list_view(self):
        """Verifica que el listado de catálogo cargue correctamente con código 200."""
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Polera Boxy 260 GSM')

    def test_product_detail_view(self):
        """Verifica la respuesta de la ficha técnica de producto."""
        response = self.client.get(reverse('catalog:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '29.990')
        self.assertContains(response, '34.990')

    def test_formatted_clp_price(self):
        """Verifica el formateo chileno del precio ($29.990)."""
        self.assertEqual(self.product.formatted_price, '$29.990')
        self.assertEqual(self.product.formatted_compare_price, '$34.990')
        self.assertTrue(self.product.has_discount)
        self.assertEqual(self.product.discount_percentage, 14)

    def test_search_api_endpoint(self):
        """Verifica que la API de búsqueda en vivo con debounce retorne resultados en JSON."""
        response = self.client.get(reverse('catalog:search_api') + '?q=Boxy')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertGreater(len(data['results']), 0)
        self.assertEqual(data['results'][0]['slug'], self.product.slug)
