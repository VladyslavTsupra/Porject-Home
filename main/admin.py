from django.contrib import admin

from main.models import AboutPage, IndexPage


# Admin for a page where only the single record can be edited.
class SingletonPageAdmin(admin.ModelAdmin):
    # Allows adding a record only when none exists yet.
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    # Forbids deleting the page record.
    def has_delete_permission(self, request, obj=None):
        return False


# Admin for editing the home page.
@admin.register(IndexPage)
class IndexPageAdmin(SingletonPageAdmin):
    list_display = ["title", "content"]


# Admin for editing the About us page.
@admin.register(AboutPage)
class AboutPageAdmin(SingletonPageAdmin):
    list_display = ["title", "content"]
