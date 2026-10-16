"""
Encabezado: Modelos de datos para el catálogo de streetwear de NORTE Studio (demo-sw).
Define la estructura de Categorías, Colecciones, Productos, Variantes de Color, Tallas con control de Stock
y Reseñas de clientes verificados, con precios en Pesos Chilenos (CLP).
"""
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """
    Representa una categoría de prendas (ej: Hoodies, Poleras Boxy, Baggy Pants).
    Permite clasificar los productos y asignarles el tipo de prenda para las ilustraciones vectoriales SVG.
    """
    GARMENT_CHOICES = [
        ('hoodie', 'Hoodie Oversized / Heavyweight'),
        ('tee', 'Polera Boxy Fit'),
        ('zip', 'Polerón Zip Up'),
        ('knit', 'Sweater Knit Texturizado'),
        ('pants', 'Pantalón Baggy / Cargo'),
        ('jacket', 'Chaqueta / Bomber / Cuero'),
        ('beanie', 'Gorro Beanie / Accesorio'),
    ]

    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name='Nombre de categoría',
        help_text='Nombre visible de la categoría, por ejemplo "Hoodies"'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Slug URL',
        help_text='Identificador amigable en la URL, en español (ej: "hoodies")'
    )
    tagline = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Frase destacada',
        help_text='Breve lema de categoría, ej: "Básicos de 450 GSM hechos para durar"'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción editorial'
    )
    garment_type = models.CharField(
        max_length=20,
        choices=GARMENT_CHOICES,
        default='hoodie',
        verbose_name='Tipo de prenda SVG',
        help_text='Determina el molde vectorial que se dibuja si no hay fotografía real'
    )
    default_color_hex = models.CharField(
        max_length=7,
        default='#161616',
        verbose_name='Color hexadecimal por defecto',
        help_text='Color de previsualización para banners y posters (ej: #161616)'
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Orden de visualización'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='¿Está activa?'
    )

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['order', 'name']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        """Retorna la URL canónica del listado filtrado por esta categoría."""
        return reverse('catalog:category_detail', kwargs={'category_slug': self.slug})


class Collection(models.Model):
    """
    Representa un lanzamiento o cápsula temporal de streetwear (ej: "Drop 01 - Invierno").
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del Drop / Colección'
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name='Slug URL'
    )
    tagline = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Lema del Drop'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Manifiesto / Descripción'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='¿Lanzamiento activo?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = 'Colección'
        verbose_name_plural = 'Colecciones'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        """Retorna la URL canónica del listado filtrado por colección."""
        return reverse('catalog:collection_detail', kwargs={'collection_slug': self.slug})


class Product(models.Model):
    """
    Modelo central de producto de ropa streetwear.
    Almacena especificaciones técnicas de confección (gramaje, corte, cuidados),
    precio en CLP, soporte para fotos reales o fallback automático a ilustración SVG interactiva.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Categoría'
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Colección / Drop'
    )
    name = models.CharField(
        max_length=150,
        verbose_name='Nombre de la prenda',
        help_text='Ej: Hoodie Heavyweight Boxy 450 GSM'
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        verbose_name='Slug URL en español'
    )
    subtitle = models.CharField(
        max_length=160,
        blank=True,
        verbose_name='Subtítulo / Fit',
        help_text='Ej: Corte cuadrado, hombros caídos y capucha sin cordones'
    )
    description = models.TextField(
        verbose_name='Descripción detallada de la prenda'
    )
    # Precios en Pesos Chilenos (CLP) sin decimales
    price_clp = models.PositiveIntegerField(
        verbose_name='Precio de venta (CLP)',
        help_text='Valor en pesos chilenos, ej: 49990'
    )
    compare_price_clp = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Precio anterior / comparativa (CLP)',
        help_text='Opcional. Si es mayor que el precio de venta, se muestra como oferta'
    )
    # Especificaciones técnicas de moda urbana
    fabric_details = models.CharField(
        max_length=200,
        default='100% Algodón Peinado Peruano 450 GSM',
        verbose_name='Composición y Gramaje'
    )
    fit_details = models.CharField(
        max_length=200,
        default='Boxy fit, hombros estructurados y caída limpia',
        verbose_name='Calce / Fit'
    )
    care_instructions = models.CharField(
        max_length=250,
        default='Lavar con agua fría al revés. No usar secadora. Secar a la sombra.',
        verbose_name='Cuidados de la prenda'
    )
    garment_type = models.CharField(
        max_length=20,
        choices=Category.GARMENT_CHOICES,
        default='hoodie',
        verbose_name='Molde vectorial SVG',
        help_text='Tipo de prenda a dibujar en la ilustración SVG interactiva'
    )
    # Soporte para fotografía real: si existe se renderiza, si no, se usa el SVG
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Fotografía real (opcional)'
    )
    image_back = models.ImageField(
        upload_to='products/back/',
        blank=True,
        null=True,
        verbose_name='Fotografía trasera real (opcional)'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='¿Destacado en Home?'
    )
    is_new = models.BooleanField(
        default=True,
        verbose_name='¿Nuevo lanzamiento?'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='¿Disponible para la venta?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de publicación'
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        """Retorna la URL de la vista de detalle del producto."""
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    @property
    def formatted_price(self) -> str:
        """Formatea el precio al estándar chileno: $49.990"""
        return f"${self.price_clp:,}".replace(',', '.')

    @property
    def formatted_compare_price(self) -> str:
        """Formatea el precio de comparación al estándar chileno."""
        if self.compare_price_clp:
            return f"${self.compare_price_clp:,}".replace(',', '.')
        return ""

    @property
    def has_discount(self) -> bool:
        """Indica si el producto tiene un descuento activo."""
        return bool(self.compare_price_clp and self.compare_price_clp > self.price_clp)

    @property
    def discount_percentage(self) -> int:
        """Calcula el porcentaje entero de descuento."""
        if self.has_discount and self.compare_price_clp:
            diff = self.compare_price_clp - self.price_clp
            return int(round((diff / self.compare_price_clp) * 100))
        return 0

    @property
    def default_color(self):
        """Retorna la variante de color marcada como por defecto o la primera disponible."""
        default = self.colors.filter(is_default=True).first()
        if not default:
            default = self.colors.first()
        return default

    @property
    def total_stock(self) -> int:
        """Calcula la suma total de stock de todas las tallas."""
        return sum(size.stock for size in self.sizes.all())

    @property
    def is_in_stock(self) -> bool:
        """Indica si al menos una talla tiene unidades disponibles."""
        return any(size.stock > 0 for size in self.sizes.all())

    @property
    def average_rating(self) -> float:
        """Calcula el promedio de calificación de las reseñas (1 a 5)."""
        reviews = self.reviews.all()
        if not reviews.exists():
            return 5.0
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)


class ProductColor(models.Model):
    """
    Variante de color de una prenda streetwear.
    Asocia un nombre visible, un código hexadecimal para los selectores y SVGs,
    y una familia cromática para filtrado de catálogo.
    """
    COLOR_FAMILY_CHOICES = [
        ('sw-black', 'Negro / Carbón'),
        ('sw-chocolate', 'Chocolate / Café'),
        ('sw-melange', 'Gris Melange'),
        ('sw-navy', 'Azul Marino'),
        ('sw-burgundy', 'Burdeo / Vino'),
        ('sw-rose', 'Rosa Palo'),
        ('sw-olive', 'Verde Oliva'),
        ('sw-cream', 'Blanco Crudo'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='colors',
        verbose_name='Producto'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Nombre del color',
        help_text='Ej: Negro Carbón Lavado, Gris Melange Claro'
    )
    hex_code = models.CharField(
        max_length=7,
        default='#161616',
        verbose_name='Código Hexadecimal',
        help_text='Formato #RRGGBB, ej: #161616'
    )
    color_family = models.CharField(
        max_length=30,
        choices=COLOR_FAMILY_CHOICES,
        default='sw-black',
        verbose_name='Familia cromática'
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='¿Color principal por defecto?'
    )

    class Meta:
        verbose_name = 'Color de producto'
        verbose_name_plural = 'Colores de producto'
        ordering = ['-is_default', 'name']

    def __str__(self) -> str:
        return f"{self.product.name} - {self.name}"


class ProductSize(models.Model):
    """
    Talla y stock disponible para una prenda.
    """
    SIZE_CHOICES = [
        ('XS', 'XS (Extra Small)'),
        ('S', 'S (Small)'),
        ('M', 'M (Medium)'),
        ('L', 'L (Large)'),
        ('XL', 'XL (Extra Large)'),
        ('XXL', 'XXL (Doble Extra Large)'),
        ('UNICA', 'Talla Única (Accesorios)'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sizes',
        verbose_name='Producto'
    )
    size = models.CharField(
        max_length=10,
        choices=SIZE_CHOICES,
        default='M',
        verbose_name='Talla'
    )
    stock = models.PositiveIntegerField(
        default=12,
        verbose_name='Unidades en stock'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='¿Talla activa?'
    )

    class Meta:
        verbose_name = 'Talla y Stock'
        verbose_name_plural = 'Tallas y Stocks'
        unique_together = ('product', 'size')
        ordering = ['size']

    def __str__(self) -> str:
        return f"{self.product.name} - Talla {self.size} ({self.stock} disponibles)"


class Review(models.Model):
    """
    Reseña y valoración de clientes sobre una prenda.
    Muestra la experiencia real de ajuste, caída y calidad de la tela.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Prenda reseñada'
    )
    author_name = models.CharField(
        max_length=100,
        verbose_name='Nombre del cliente'
    )
    customer_city = models.CharField(
        max_length=80,
        default='Santiago',
        verbose_name='Ciudad / Comuna del cliente'
    )
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Puntuación (1 a 5 estrellas)'
    )
    title = models.CharField(
        max_length=120,
        verbose_name='Título de la reseña'
    )
    comment = models.TextField(
        verbose_name='Comentario sobre gramaje, calce y confección'
    )
    verified_purchase = models.BooleanField(
        default=True,
        verbose_name='¿Compra verificada?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de publicación'
    )

    class Meta:
        verbose_name = 'Reseña de Cliente'
        verbose_name_plural = 'Reseñas de Clientes'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.author_name} - {self.product.name} ({self.rating}★)"
