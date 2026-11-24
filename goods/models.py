from django.db import models
from django.urls import reverse


# Product category.
class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Category name")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")

    # Sets the table name, model labels and ordering.
    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("id",)

    # Returns the category name.
    def __str__(self):
        return self.name


# Catalog product with price, discount and stock.
class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Product name")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image = models.ImageField(
        upload_to="goods_images", blank=True, null=True, verbose_name="Image"
    )
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name="Price")
    discount = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Discount"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name="Category")

    # Sets the table name, model labels and ordering.
    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("id",)

    # Returns the product name with its quantity.
    def __str__(self):
        return f"{self.name} Quantity: {self.quantity}"

    # Returns the product page URL.
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})

    # Returns the product id padded with zeros to five digits.
    def display_id(self):
        return f"{self.id:05}"

    # Returns the product price with the discount applied.
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)

        return self.price
