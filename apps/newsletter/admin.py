"""
Encabezado: Panel de administración para apps/newsletter en demo-sw.
Permite visualizar la lista de suscriptores al boletín y exportar contactos.
"""
from django.contrib import admin
from .models import NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """Administración de suscriptores al boletín."""
    list_display = ('email', 'discount_code', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email', 'discount_code')
    readonly_fields = ('created_at',)
