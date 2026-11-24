from django.core.cache import cache
from django.db import models


# Abstract single-record page model that clears its cache after changes.
class SingletonPageModel(models.Model):
    cache_key = None

    # Makes the model abstract, so no table is created for it.
    class Meta:
        abstract = True

    # Always saves the record with pk=1 and clears the page cache.
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete(self.cache_key)

    # Deletes the record and the page cache.
    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        cache.delete(self.cache_key)
        return result


# Home page content, editable in the admin.
class IndexPage(SingletonPageModel):
    cache_key = "main_index_page"

    title = models.CharField(
        max_length=150,
        default="Home - Main page",
        verbose_name="Tab title",
    )
    content = models.CharField(
        max_length=255,
        default="Welcome to the Home main page",
        verbose_name="Page heading",
    )

    # Sets the table name and the model labels in the admin.
    class Meta:
        db_table = "index_page"
        verbose_name = "Main page"
        verbose_name_plural = "Main page"

    # Returns the record name for the admin.
    def __str__(self):
        return "Main page"


# About us page content, editable in the admin.
class AboutPage(SingletonPageModel):
    cache_key = "main_about_page"

    title = models.CharField(
        max_length=150,
        default="Home - About us",
        verbose_name="Tab title",
    )
    content = models.CharField(
        max_length=255,
        default="About us",
        verbose_name="Page heading",
    )
    text_on_page = models.TextField(
        default="We are a team of professionals who design and sell furniture.",
        verbose_name="Page text",
    )

    # Sets the table name and the model labels in the admin.
    class Meta:
        db_table = "about_page"
        verbose_name = "About us page"
        verbose_name_plural = "About us page"

    # Returns the record name for the admin.
    def __str__(self):
        return "About us page"
