from django.db import models

from goods.models import Products
from users.models import User


# Cart queryset with total price and quantity helpers.
class CartQueryset(models.QuerySet):
    # Returns the total price of all products in the carts.
    def total_price(self):
        return sum(cart.products_price() for cart in self)

    # Returns the total quantity of products in the carts.
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


# Product in the cart of a logged-in or anonymous user.
class Cart(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User"
    )
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Quantity")
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date added")

    # Sets the table name, model labels and ordering.
    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Cart"
        ordering = ("id",)

    objects = CartQueryset().as_manager()

    # Returns the product cost multiplied by the quantity.
    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    # Returns the cart description for the admin.
    def __str__(self) -> str:
        if self.user:
            return f"Cart {self.user.username} | Product {self.product.name} | Quantity {self.quantity}"

        return f"Anonymous cart | Product {self.product.name} | Quantity {self.quantity}"
