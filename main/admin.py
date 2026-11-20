from django.contrib import admin

from main.models import AboutPage, IndexPage


# Адмінка сторінки, у якій можна лише редагувати єдиний запис.
class SingletonPageAdmin(admin.ModelAdmin):
    # Дозволяє додати запис тільки тоді, коли його ще немає.
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    # Забороняє видаляти запис сторінки.
    def has_delete_permission(self, request, obj=None):
        return False


# Адмінка для редагування головної сторінки.
@admin.register(IndexPage)
class IndexPageAdmin(SingletonPageAdmin):
    list_display = ["title", "content"]


# Адмінка для редагування сторінки «О нас».
@admin.register(AboutPage)
class AboutPageAdmin(SingletonPageAdmin):
    list_display = ["title", "content"]
