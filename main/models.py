from django.core.cache import cache
from django.db import models


# Абстрактна модель сторінки з одним записом, яка очищує свій кеш після змін.
class SingletonPageModel(models.Model):
    cache_key = None

    # Робить модель абстрактною, тому для неї не створюється таблиця.
    class Meta:
        abstract = True

    # Зберігає запис завжди з pk=1 і видаляє кеш сторінки.
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete(self.cache_key)

    # Видаляє запис і кеш сторінки.
    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        cache.delete(self.cache_key)
        return result


# Вміст головної сторінки, який редагується в адмінці.
class IndexPage(SingletonPageModel):
    cache_key = "main_index_page"

    title = models.CharField(
        max_length=150,
        default="Home - Главная страница",
        verbose_name="Заголовок вкладки (title)",
    )
    content = models.CharField(
        max_length=255,
        default="Добро пожаловать на главную страницу сайта Home",
        verbose_name="Заголовок на странице",
    )

    # Задає назву таблиці та підписи моделі в адмінці.
    class Meta:
        db_table = "index_page"
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"

    # Повертає назву запису для адмінки.
    def __str__(self):
        return "Главная страница"


# Вміст сторінки «О нас», який редагується в адмінці.
class AboutPage(SingletonPageModel):
    cache_key = "main_about_page"

    title = models.CharField(
        max_length=150,
        default="Home - О нас",
        verbose_name="Заголовок вкладки (title)",
    )
    content = models.CharField(
        max_length=255,
        default="О нас",
        verbose_name="Заголовок на странице",
    )
    text_on_page = models.TextField(
        default="Мы - команда профессионалов, которая занимается разработкой и продажей мебели.",
        verbose_name="Текст на странице",
    )

    # Задає назву таблиці та підписи моделі в адмінці.
    class Meta:
        db_table = "about_page"
        verbose_name = "Страница «О нас»"
        verbose_name_plural = "Страница «О нас»"

    # Повертає назву запису для адмінки.
    def __str__(self):
        return "Страница «О нас»"
