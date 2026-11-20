from django.db import models
from django.urls import reverse


# Категорія товарів.
class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")

    # Задає назву таблиці, підписи моделі та сортування.
    class Meta:
        db_table = "category"
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"
        ordering = ("id",)

    # Повертає назву категорії.
    def __str__(self):
        return self.name


# Товар каталогу з ціною, знижкою і залишком.
class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="goods_images", blank=True, null=True, verbose_name="Изображение"
    )
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена")
    discount = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Скидка"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name="Категория")

    # Задає назву таблиці, підписи моделі та сортування.
    class Meta:
        db_table = "products"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("id",)

    # Повертає назву товару з кількістю.
    def __str__(self):
        return f"{self.name} Количество: - {self.quantity}"

    # Повертає URL сторінки товару.
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})

    # Повертає id товару, доповнений нулями до п'яти цифр.
    def display_id(self):
        return f"{self.id:05}"

    # Повертає ціну товару з урахуванням знижки.
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)

        return self.price
