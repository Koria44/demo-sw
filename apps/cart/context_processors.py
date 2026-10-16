"""
Encabezado: Procesador de contexto para el carrito de compras en demo-sw.
Inyecta la instancia de Cart en todas las plantillas Django, permitiendo que el contador del header,
el drawer lateral y los badges de cantidad funcionen globalmente sin recargar.
"""
from .cart import Cart

def cart_context(request):
    """
    Procesador de contexto que retorna el carrito activo de la sesión del usuario.

    Args:
        request: HttpRequest actual.

    Returns:
        dict: Diccionario con la clave 'cart' disponible en todas las plantillas.
    """
    return {
        'cart': Cart(request)
    }
