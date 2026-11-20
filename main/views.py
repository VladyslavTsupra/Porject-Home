from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import AboutPage, IndexPage

PAGE_CACHE_TIME = 60 * 60  # 1 година; кеш також скидається при збереженні в адмінці
NOT_FOUND_TITLE = "Home - Страница не найдена"


# Міксин, який бере дані сторінки з кешу і звертається до БД лише за їх відсутності.
class PageCacheMixin:
    page_model = None

    # Повертає запис сторінки з кешу або створює його зі значеннями за замовчуванням.
    def get_page(self):
        page = cache.get(self.page_model.cache_key)
        if page is None:
            page, _ = self.page_model.objects.get_or_create(pk=1)
            cache.set(self.page_model.cache_key, page, PAGE_CACHE_TIME)
        return page


# Контролер головної сторінки.
class IndexView(PageCacheMixin, TemplateView):
    template_name = "main/index.html"
    page_model = IndexPage

    # Додає в контекст заголовок і текст головної сторінки.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_page()
        context["title"] = page.title
        context["content"] = page.content
        return context


# Контролер сторінки «О нас».
class AboutView(PageCacheMixin, TemplateView):
    template_name = "main/about.html"
    page_model = AboutPage

    # Додає в контекст заголовок і текст сторінки «О нас».
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_page()
        context["title"] = page.title
        context["content"] = page.content
        context["text_on_page"] = page.text_on_page
        return context


# Контролер сторінок, які ще не готові, і показує для них сторінку 404.
class PageNotFoundView(TemplateView):
    template_name = "404.html"
    extra_context = {"title": NOT_FOUND_TITLE}

    # Повертає сторінку 404 з відповідним HTTP-статусом.
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs), status=404)


# Обробник 404 для всіх неіснуючих адрес, коли DEBUG = False.
def page_not_found(request, exception):
    return render(request, "404.html", {"title": NOT_FOUND_TITLE}, status=404)
