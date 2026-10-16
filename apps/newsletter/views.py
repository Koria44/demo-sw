"""
Encabezado: Vistas para suscripción al Newsletter en demo-sw.
Valida el correo, almacena el registro y entrega feedback amigable con cupón de bienvenida.
"""
from django.shortcuts import redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import NewsletterSubscriber


@require_POST
def subscribe_view(request):
    """
    Procesa la suscripción al newsletter vía POST tradicional o AJAX.
    """
    email = request.POST.get('email', '').strip().lower()
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if not email:
        msg = 'Por favor ingresa tu correo electrónico.'
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg}, status=400)
        messages.error(request, msg)
        return redirect(request.META.get('HTTP_REFERER', '/'))

    try:
        validate_email(email)
    except ValidationError:
        msg = 'Ingresa un formato de correo electrónico válido (ejemplo: usuario@correo.cl).'
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg}, status=400)
        messages.error(request, msg)
        return redirect(request.META.get('HTTP_REFERER', '/'))

    subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)

    if created:
        msg = f'¡Bienvenido a la comunidad! Usa el código {subscriber.discount_code} para un 10% OFF en tu primera compra.'
    else:
        msg = f'Ya estás registrado con este correo. Recuerda usar tu cupón de bienvenida: {subscriber.discount_code}.'

    if is_ajax:
        return JsonResponse({
            'success': True,
            'message': msg,
            'discount_code': subscriber.discount_code
        })

    messages.success(request, msg)
    return redirect(request.META.get('HTTP_REFERER', '/'))
