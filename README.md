HOME

Інтернет магазин меблів на джанго,

Що є:
каталог з категоріями, фільтр по знижці, сортування по ціні і пагінація
пошук по назві, опису або по id товару (через триграми в postgres)
реєстрація, вхід, профіль з аватаркою і історією замовлень
кошик на ajax, працює і без реєстрації, після входу кошик переноситься в акаунт
оформлення замовлення з доставкою або самовивозом, перевіряє чи є товар на складі
адмінка, там можна міняти товари, замовлення і текст на головній і на сторінці про нас
кеш для меню категорій, замовлень і головної
своя сторінка 404

Використав python 3.14, django 6.1, postgresql, bootstrap, jquery, uv, ruff, debug toolbar

Як запустити:
треба postgres з базою home, юзер і пароль теж home (все в config/settings.py)

uv sync
uv run python manage.py migrate
uv run python manage.py loaddata fixtures/goods/categories.json fixtures/goods/products.json
uv run python manage.py createsuperuser
uv run python manage.py runserver

потім відкрити http://127.0.0.1:8000, адмінка на /admin/

картинки товарів лежать в media, вона в гіт не йде, тому їх треба закинути окремо


