#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos (CSS/JS)
python manage.py collectstatic --no-input

# EJECUTAR MIGRACIONES (Esto reemplaza al Shell pagado)
python manage.py migrate