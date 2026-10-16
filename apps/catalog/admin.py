"""
Encabezado: Configuración del panel de administración de Django para apps/catalog.
Permite gestionar de forma intuitiva los productos streetwear, sus variantes de color y stock,
con slugs prepopulados automáticamente y vistas tabulares de edición inline.
"""
from django.contrib import admin
from .models import Category, Collection, Product, ProductColor, ProductSize, Review


class ProductColorInline(admin.TabularInline):
    """Edición inline de colores disponibles para una prenda."""
    model = ProductColor
    extra = 1
    fields = ('name', 'hex_code', 'color_family', 'is_default')


class ProductSizeInline(admin.TabularInline):
    """Edición inline de tallas y stock para una prenda."""
    model = ProductSize
    extra = 1
    fields = ('size', 'stock', 'is_active')


class ReviewInline(admin.TabularInline):
    """Visualización y moderación inline de reseñas."""
    model = Review
    extra = 0
    fields = ('author_name', 'customer_city', 'rating', 'title', 'verified_purchase', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administración de categorías del catálogo."""
    list_display = ('name', 'slug', 'garment_type', 'default_color_hex', 'order', 'is_active')
    list_editable = ('order', 'is_active', 'garment_type')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'garment_type')


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """Administración de colecciones y drops."""
    list_display = ('name', 'slug', 'tagline', 'is_active', 'created_at')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'tagline')
    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Administración de productos streetwear con variantes inline."""
    list_display = (
        'name',
        'category',
        'formatted_price',
        'garment_type',
        'is_featured',
        'is_new',
        'is_active',
        'created_at'
    )
    list_filter = ('is_active', 'is_featured', 'is_new', 'category', 'collection', 'garment_type')
    list_editable = ('is_featured', 'is_new', 'is_active')
    search_fields = ('name', 'slug', 'description', 'fabric_details', 'fit_details')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductColorInline, ProductSizeInline, ReviewInline]
    fieldsets = (
        ('Identificación de la Prenda', {
            'fields': ('name', 'slug', 'subtitle', 'category', 'collection', 'garment_type')
        }),
        ('Precios en CLP y Descuentos', {
            'fields': ('price_clp', 'compare_price_clp')
        }),
        ('Ficha Técnica y Confección', {
            'fields': ('description', 'fabric_details', 'fit_details', 'care_instructions')
        }),
        ('Fotografías Reales (Opcional)', {
            'description': 'Si no se sube foto real, se renderiza automáticamente la ilustración SVG paramétrica.',
            'fields': ('image', 'image_back')
        }),
        ('Visibilidad y Destacados', {
            'fields': ('is_featured', 'is_new', 'is_active')
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Administración de reseñas de clientes."""
    list_display = ('author_name', 'product', 'rating', 'title', 'customer_city', 'verified_purchase', 'created_at')
    list_filter = ('rating', 'verified_purchase', 'created_at')
    search_fields = ('author_name', 'product__name', 'title', 'comment')
