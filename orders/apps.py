from django.apps import AppConfig


# Конфігурація застосунку orders.
class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"
    verbose_name = "Заказы"
