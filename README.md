HOME

Live demo: https://home-shop-n997.onrender.com
(free hosting, the first load can take up to a minute)

A furniture online store built with Django.

Features:
- catalog with categories, discount filter, price sorting and pagination
- search by name, description or product id (PostgreSQL trigrams)
- registration, login, profile with avatar and order history
- AJAX cart that works without registration; after login the cart moves to the account
- checkout with delivery or pickup, with a stock check
- admin panel to manage products, orders and the text on the home and About us pages
- caching for the category menu, orders and the home page
- custom 404 page

Stack: Python 3.14, Django 6.1, PostgreSQL, Bootstrap, jQuery, uv, ruff, Django Debug Toolbar

How to run locally:
you need PostgreSQL with a database named home (user and password are also home)

cp .env.example .env    (then fill in your values)
uv sync
uv run python manage.py migrate
uv run python manage.py loaddata fixtures/goods/categories.json fixtures/goods/products.json
uv run python manage.py createsuperuser
uv run python manage.py runserver

then open http://127.0.0.1:8000, the admin panel is at /admin/

Deployment:
database - Neon (neon.tech), web app - Render (render.com), configured in render.yaml and build.sh
on Render: New -> Blueprint -> this repository, set DATABASE_URL from Neon and the admin password
the free instance sleeps after 15 minutes without requests, so the first load takes about a minute
