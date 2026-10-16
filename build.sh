#!/usr/bin/env bash
# ==============================================================================
# Script de construcción y despliegue automático en Render para demo-sw
# ==============================================================================
# Detiene la ejecución si ocurre cualquier error
set -o errexit

echo "==> 1. Instalando dependencias de Python..."
pip install -r requirements.txt

echo "==> 2. Instalando dependencias de Node.js y compilando Tailwind CSS..."
npm install
npm run build

echo "==> 3. Recolectando archivos estáticos para WhiteNoise..."
python manage.py collectstatic --no-input

echo "==> 4. Aplicando migraciones de base de datos..."
python manage.py migrate

echo "==> 5. Poblando catálogo inicial de demostración..."
python manage.py seed_demo

echo "==> ¡Construcción finalizada con éxito!"
