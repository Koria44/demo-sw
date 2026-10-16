"""
Encabezado: Motor de gestión de Carrito de Compras en sesión para demo-sw.
Maneja la adición, actualización y eliminación de prendas, validando selección de talla,
calculando subtotales en Pesos Chilenos (CLP) y monitoreando el progreso hacia el despacho gratis ($70.000 CLP).
"""
from decimal import Decimal
from django.conf import settings
from apps.catalog.models import Product, ProductColor, ProductSize


class Cart:
    """
    Controlador del carrito de compras basado en la sesión HTTP de Django.
    Permite operar de forma anónima (sin necesidad de iniciar sesión o registrarse).
    """
    def __init__(self, request):
        """
        Inicializa el carrito extrayendo la estructura existente de la sesión
        o creando un diccionario vacío si el visitante es nuevo.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def _get_item_key(self, product_id: int, size: str, color_id: int) -> str:
        """Genera una clave compuesta única para cada variante de producto, talla y color."""
        return f"{product_id}_{size}_{color_id}"

    def add(self, product: Product, size: str, color_id: int, quantity: int = 1, override_quantity: bool = False) -> dict:
        """
        Agrega un producto al carrito o incrementa su cantidad.

        Args:
            product (Product): Instancia de la prenda a agregar.
            size (str): Talla seleccionada (ej: 'M', 'L').
            color_id (int): ID de la variante de color seleccionada.
            quantity (int): Número de unidades a añadir.
            override_quantity (bool): Si es True, reemplaza la cantidad en lugar de sumar.

        Returns:
            dict: Datos del ítem registrado en el carrito.
        """
        item_key = self._get_item_key(product.id, size, color_id)

        # Resuelve la variante de color o toma la predeterminada si no existe
        color = ProductColor.objects.filter(id=color_id, product=product).first()
        color_name = color.name if color else 'Estándar'
        color_hex = color.hex_code if color else '#161616'

        if item_key not in self.cart:
            self.cart[item_key] = {
                'product_id': product.id,
                'name': product.name,
                'slug': product.slug,
                'size': size,
                'color_id': color_id,
                'color_name': color_name,
                'color_hex': color_hex,
                'garment_type': product.garment_type,
                'price_clp': int(product.price_clp),
                'quantity': 0,
                'has_image': bool(product.image),
                'image_url': product.image.url if product.image else '',
            }

        if override_quantity:
            self.cart[item_key]['quantity'] = max(1, quantity)
        else:
            self.cart[item_key]['quantity'] += quantity

        self.save()
        return self.cart[item_key]

    def update_quantity(self, item_key: str, quantity: int):
        """Modifica la cantidad de un ítem existente o lo remueve si la cantidad es 0 o menor."""
        if item_key in self.cart:
            if quantity > 0:
                self.cart[item_key]['quantity'] = quantity
            else:
                del self.cart[item_key]
            self.save()

    def remove(self, item_key: str):
        """Elimina un ítem específico del carrito."""
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def clear(self):
        """Vacía por completo el carrito de compras de la sesión."""
        self.session[settings.CART_SESSION_ID] = {}
        self.save()

    def save(self):
        """Marca la sesión de Django como modificada para asegurar su persistencia en cookies."""
        self.session.modified = True

    def __iter__(self):
        """
        Itera sobre los elementos del carrito, sincronizando los datos con la base de datos
        para obtener precios actualizados y calcular subtotales por línea.
        """
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids).in_bulk()

        for key, item in list(self.cart.items()):
            product = products.get(item['product_id'])
            if not product:
                # Si el producto fue eliminado del catálogo, lo quitamos silenciosamente del carrito
                continue

            item_copy = item.copy()
            item_copy['item_key'] = key
            item_copy['product'] = product
            # Actualizamos el precio por si cambió en catálogo
            item_copy['price_clp'] = product.price_clp
            item_copy['line_total_clp'] = product.price_clp * item['quantity']
            item_copy['formatted_price'] = f"${product.price_clp:,}".replace(',', '.')
            item_copy['formatted_line_total'] = f"${item_copy['line_total_clp']:,}".replace(',', '.')
            yield item_copy

    def __len__(self) -> int:
        """Devuelve la cantidad total de prendas individuales en el carrito."""
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total_items(self) -> int:
        """Alias legible para la cantidad de unidades."""
        return len(self)

    @property
    def subtotal_clp(self) -> int:
        """Calcula el subtotal acumulado de las prendas en Pesos Chilenos."""
        return sum(item['price_clp'] * item['quantity'] for item in self.cart.values())

    @property
    def formatted_subtotal(self) -> str:
        """Formatea el subtotal en formato chileno: $49.990"""
        return f"${self.subtotal_clp:,}".replace(',', '.')

    @property
    def free_shipping_threshold(self) -> int:
        """Monto mínimo en CLP para despacho gratuito."""
        return getattr(settings, 'FREE_SHIPPING_THRESHOLD', 70000)

    @property
    def qualifies_for_free_shipping(self) -> bool:
        """Determina si la compra califica para despacho gratis a todo Chile."""
        return self.subtotal_clp >= self.free_shipping_threshold

    @property
    def remaining_for_free_shipping(self) -> int:
        """Calcula los pesos restantes para alcanzar el despacho gratuito."""
        diff = self.free_shipping_threshold - self.subtotal_clp
        return max(0, diff)

    @property
    def formatted_remaining_for_free_shipping(self) -> str:
        """Formatea el monto restante para envío gratis."""
        return f"${self.remaining_for_free_shipping:,}".replace(',', '.')

    @property
    def free_shipping_progress_percentage(self) -> int:
        """Calcula el porcentaje de progreso (0% a 100%) hacia el despacho gratis."""
        if self.subtotal_clp == 0:
            return 0
        if self.qualifies_for_free_shipping:
            return 100
        progress = int((self.subtotal_clp / self.free_shipping_threshold) * 100)
        return min(100, max(5, progress))

    @property
    def standard_shipping_cost(self) -> int:
        """Retorna el costo de despacho: 0 si califica a envío gratis, o el costo fijo."""
        if self.qualifies_for_free_shipping or self.total_items == 0:
            return 0
        return getattr(settings, 'STANDARD_SHIPPING_COST', 3990)

    @property
    def formatted_shipping_cost(self) -> str:
        """Retorna el costo de envío formateado o 'GRATIS'."""
        if self.standard_shipping_cost == 0:
            return "GRATIS"
        return f"${self.standard_shipping_cost:,}".replace(',', '.')

    @property
    def total_clp(self) -> int:
        """Calcula el total final sumando el subtotal y el despacho aplicable."""
        if self.total_items == 0:
            return 0
        return self.subtotal_clp + self.standard_shipping_cost

    @property
    def formatted_total(self) -> str:
        """Formatea el monto total en CLP."""
        return f"${self.total_clp:,}".replace(',', '.')

    def to_dict(self) -> dict:
        """Exporta un resumen serializable en JSON para el frontend interactivo."""
        items = list(self)
        return {
            'total_items': self.total_items,
            'subtotal_clp': self.subtotal_clp,
            'formatted_subtotal': self.formatted_subtotal,
            'qualifies_for_free_shipping': self.qualifies_for_free_shipping,
            'remaining_for_free_shipping': self.remaining_for_free_shipping,
            'formatted_remaining_for_free_shipping': self.formatted_remaining_for_free_shipping,
            'free_shipping_progress_percentage': self.free_shipping_progress_percentage,
            'standard_shipping_cost': self.standard_shipping_cost,
            'formatted_shipping_cost': self.formatted_shipping_cost,
            'total_clp': self.total_clp,
            'formatted_total': self.formatted_total,
            'items': [
                {
                    'item_key': it['item_key'],
                    'product_id': it['product_id'],
                    'name': it['name'],
                    'slug': it['slug'],
                    'size': it['size'],
                    'color_name': it['color_name'],
                    'color_hex': it['color_hex'],
                    'garment_type': it['garment_type'],
                    'quantity': it['quantity'],
                    'price_clp': it['price_clp'],
                    'formatted_price': it['formatted_price'],
                    'line_total_clp': it['line_total_clp'],
                    'formatted_line_total': it['formatted_line_total'],
                    'has_image': it['has_image'],
                    'image_url': it['image_url'],
                }
                for it in items
            ]
        }
