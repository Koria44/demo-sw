"""
Encabezado: Formulario de checkout y validación de despacho para demo-sw.
Valida datos de contacto, formato de RUT chileno, teléfono, región y comuna,
aplicando estilos de Tailwind CSS consistentes con la estética sobria de la tienda.
"""
import re
from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    """
    Formulario de procesamiento de orden y captura de datos de despacho en Chile.
    """
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'rut',
            'region',
            'comuna',
            'address_line',
            'apartment_or_office',
            'delivery_notes',
            'payment_method',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full bg-bone-light border border-bone-dark px-4 py-3 text-sm text-dark focus:border-dark focus:outline-none transition-colors rounded-none',
                'placeholder': 'Ej: Benjamín',
                'required': True,
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full bg-bone-light border border-bone-dark px-4 py-3 text-sm text-dark focus:border-dark focus:outline-none transition-colors rounded-none',
                'placeholder': 'Ej: González',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-bone-light border border-bone-dark px-4 py-3 text-sm text-dark focus:border-dark focus:outline-none transition-colors rounded-none',
                'placeholder': 'nombre@ejemplo.cl',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full bg-bone-light border border-bone-dark px-4 py-3 text-sm text-dark focus:border-dark focus:outline-none transition-colors rounded-none',
                'placeholder': '+56 9 1234 5678',
                'required': True,
            }),
            'rut': forms.TextInput(attrs={
                'class': 'w-full bg-bone-light border border-bone-dark px-4 py-3 text-sm text-dark focus:border-dark focus:outline-none transition-colors rounded-none',
                'placeholder': '12.345.678-9',
                'required': True,
            }),
            'region': forms.Select(attrs={
                'class': 'w-full bg-bone-light border border-bone-dark px-4 py-3 text-sm text-dark focus:border-dark focus:outline-none transition-colors rounded-none',
                'required': True,
            }),
            'comuna': forms.TextInput(attrs={
                'class': 'w-full bg-bone-light border border-bone-dark px-4 py-3 text-sm text-dark focus:border-dark focus:outline-none transition-colors rounded-none',
                'placeholder': 'Ej: Providencia, Las Condes, Viña del Mar',
                'required': True,
            }),
            'address_line': forms.TextInput(attrs={
                'class': 'w-full bg-bone-light border border-bone-dark px-4 py-3 text-sm text-dark focus:border-dark focus:outline-none transition-colors rounded-none',
                'placeholder': 'Ej: Av. Providencia 1234',
                'required': True,
            }),
            'apartment_or_office': forms.TextInput(attrs={
                'class': 'w-full bg-bone-light border border-bone-dark px-4 py-3 text-sm text-dark focus:border-dark focus:outline-none transition-colors rounded-none',
                'placeholder': 'Depto 402, Torre B (opcional)',
            }),
            'delivery_notes': forms.Textarea(attrs={
                'class': 'w-full bg-bone-light border border-bone-dark px-4 py-3 text-sm text-dark focus:border-dark focus:outline-none transition-colors rounded-none resize-none',
                'rows': 3,
                'placeholder': 'Dejar en conserjería, llamar antes de llegar...',
            }),
            'payment_method': forms.RadioSelect(attrs={
                'class': 'text-dark focus:ring-dark',
            }),
        }

    def clean_rut(self):
        """
        Limpia y valida que el RUT chileno tenga formato coherente.
        Permite caracteres con o sin puntos y guion.
        """
        raw_rut = self.cleaned_data.get('rut', '').strip().upper()
        # Remueve puntos y espacios
        cleaned = re.sub(r'[\.\s]', '', raw_rut)

        # Verifica formato mínimo de largo (ej: 1234567-K o 12345678-9)
        pattern = r'^\d{7,8}-[\dK]$'
        if not re.match(pattern, cleaned):
            raise forms.ValidationError(
                'Por favor ingresa un RUT chileno válido con guion (ejemplo: 12.345.678-9).'
            )
        return cleaned

    def clean_phone(self):
        """Valida que el número telefónico contenga dígitos representativos."""
        phone = self.cleaned_data.get('phone', '').strip()
        digits = re.sub(r'\D', '', phone)
        if len(digits) < 8:
            raise forms.ValidationError(
                'Ingresa un número telefónico de contacto válido (mínimo 8 dígitos).'
            )
        return phone
