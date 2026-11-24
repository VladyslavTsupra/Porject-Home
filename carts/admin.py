from django.contrib import admin

from carts.models import Cart


# Inline carts table for the user page in the admin.
class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ["product", "quantity", "created_timestamp"]
    search_fields = ["product", "quantity", "created_timestamp"]
    readonly_fields = ("created_timestamp",)
    extra = 1


# Admin for viewing and filtering carts.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user_display", "product_display", "quantity", "created_timestamp"]
    list_filter = ["created_timestamp", "user", "product__name"]

    # Returns the username or an anonymous cart label.
    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Anonymous user"

    # Returns the name of the product in the cart.
    def product_display(self, obj):
        return str(obj.product.name)

    # user_display and product_display alter name of columns in admin panel
    user_display.short_description = "User"
    product_display.short_description = "Product"
