from django.contrib import admin

from carts.models import Cart


# Вбудована таблиця кошиків для сторінки користувача в адмінці.
class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ["product", "quantity", "created_timestamp"]
    search_fields = ["product", "quantity", "created_timestamp"]
    readonly_fields = ("created_timestamp",)
    extra = 1


# Адмінка для перегляду і фільтрації кошиків.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user_display", "product_display", "quantity", "created_timestamp"]
    list_filter = ["created_timestamp", "user", "product__name"]

    # Повертає ім'я користувача або позначку анонімного кошика.
    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимний пользователь"

    # Повертає назву товару в кошику.
    def product_display(self, obj):
        return str(obj.product.name)

    # user_display and product_display alter name of columns in admin panel
    user_display.short_description = "Пользователь"
    product_display.short_description = "Товар"
