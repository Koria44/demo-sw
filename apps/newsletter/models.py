"""
Encabezado: Modelo de Suscriptores de Newsletter para demo-sw (NORTE Studio).
Almacena correos suscritos y el estado de entrega del beneficio de 10% de descuento.
"""
from django.db import models


class NewsletterSubscriber(models.Model):
    """
    Representa un correo registrado en el boletín para recibir noticias de drops y descuentos.
    """
    email = models.EmailField(
        unique=True,
        verbose_name='Correo Electrónico'
    )
    discount_code = models.CharField(
        max_length=30,
        default='NORTE10',
        verbose_name='Código de descuento asignado'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='¿Suscripción activa?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )

    class Meta:
        verbose_name = 'Suscriptor de Newsletter'
        verbose_name_plural = 'Suscriptores de Newsletter'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.email
