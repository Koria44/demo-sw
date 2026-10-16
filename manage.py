#!/usr/bin/env python
"""
Encabezado: Script de gestión de comandos para el proyecto demo-sw.
Punto de entrada de línea de comandos para tareas administrativas de Django.
Configura el módulo de configuración por defecto apuntando a config.settings.dev.
"""
import os
import sys

def main():
    """Ejecuta tareas administrativas de Django."""
    # Selecciona el entorno de configuración (por defecto dev para desarrollo local)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. Asegúrate de que tu entorno virtual esté activado "
            "y que las dependencias estén instaladas con 'pip install -r requirements.txt'."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
