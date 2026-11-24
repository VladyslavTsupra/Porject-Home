from django.contrib import admin

from goods.models import Categories, Products


# Categories admin with slug autofill.
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = [
        "name",
    ]


# Products admin with search, filters and inline discount editing.
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "quantity", "price", "discount"]
    list_editable = ["discount"]
    search_fields = ["name", "description"]
    list_filter = ["discount", "quantity", "category"]
    fields = ["name", "category", "slug", "description", "image", ("price", "discount"), "quantity"]
