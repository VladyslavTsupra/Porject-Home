#!/usr/bin/env bash
# Скрипт збірки для Render
set -o errexit

pip install uv
uv sync --frozen --no-dev

uv run python manage.py collectstatic --no-input
uv run python manage.py migrate --no-input

# Демо-дані: товари і категорії (повторне завантаження просто оновлює записи)
uv run python manage.py loaddata fixtures/goods/categories.json fixtures/goods/products.json

# Демо-адмін з DJANGO_SUPERUSER_USERNAME / _PASSWORD / _EMAIL (якщо вже є — пропускаємо)
uv run python manage.py createsuperuser --no-input || true
