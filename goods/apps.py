from django.apps import AppConfig


# Конфігурація застосунку goods.
class GoodsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "goods"
    verbose_name = "Товары"
