#!/usr/bin/env bash
# Build script for Render
set -o errexit

pip install uv
uv sync --frozen --no-dev

uv run python manage.py collectstatic --no-input
uv run python manage.py migrate --no-input

# Demo data: products and categories (reloading just updates the records)
uv run python manage.py loaddata fixtures/goods/categories.json fixtures/goods/products.json

# Demo admin from DJANGO_SUPERUSER_USERNAME / _PASSWORD / _EMAIL (skipped if it already exists)
uv run python manage.py createsuperuser --no-input || true
