from typing import Any

from django.db import models

from goods.models import Products
from users.models import User


# Order items queryset with total price and quantity helpers.
class OrderItemQueryset(models.QuerySet):
    # Returns the total price of the order items.
    def total_price(self):
        return sum(cart.products_price() for cart in self)

    # Returns the total quantity of the order items.
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


# User order with delivery and payment details.
class Order(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        verbose_name="User",
        default=None,
    )
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Order date")
    phone_number = models.CharField(max_length=20, verbose_name="Phone number")
    requires_delivery = models.BooleanField(default=False, verbose_name="Delivery required")
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Delivery address")
    payment_on_get = models.BooleanField(default=False, verbose_name="Payment on delivery")
    is_paid = models.BooleanField(default=False, verbose_name="Paid")
    status = models.CharField(max_length=50, default="Processing", verbose_name="Order status")

    # Sets the table name, model labels and ordering.
    class Meta:
        db_table: str = "order"
        verbose_name: str = "Order"
        verbose_name_plural: str = "Orders"
        ordering = ("id",)

    # Returns the order description for the admin.
    def __str__(self) -> str:
        return f"Order #{self.pk} | Customer {self.user.first_name} {self.user.last_name}"


# Order item with the price at the time of purchase.
class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Order")
    product = models.ForeignKey(
        to=Products, on_delete=models.SET_DEFAULT, null=True, verbose_name="Product", default=None
    )
    name = models.CharField(max_length=150, verbose_name="Name")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Price")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date sold")

    # Sets the table name, model labels and ordering.
    class Meta:
        db_table: str = "order_item"
        verbose_name: str = "Sold item"
        verbose_name_plural: str = "Sold items"
        ordering = ("id",)

    objects = OrderItemQueryset.as_manager()

    # Returns the product cost multiplied by the quantity.
    def products_price(self) -> Any:
        return round(self.price * self.quantity, 2)

    # Returns the order item description.
    def __str__(self) -> str:
        return f"Product {self.name} | Order #{self.order.pk}"
