from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import AboutPage, IndexPage

PAGE_CACHE_TIME = 60 * 60  # 1 hour; the cache is also cleared when saving in the admin
NOT_FOUND_TITLE = "Home - Page not found"


# Mixin that takes page data from the cache and queries the DB only when it is missing.
class PageCacheMixin:
    page_model = None

    # Returns the page record from the cache or creates it with default values.
    def get_page(self):
        page = cache.get(self.page_model.cache_key)
        if page is None:
            page, _ = self.page_model.objects.get_or_create(pk=1)
            cache.set(self.page_model.cache_key, page, PAGE_CACHE_TIME)
        return page


# Home page view.
class IndexView(PageCacheMixin, TemplateView):
    template_name = "main/index.html"
    page_model = IndexPage

    # Adds the home page title and text to the context.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_page()
        context["title"] = page.title
        context["content"] = page.content
        return context


# About us page view.
class AboutView(PageCacheMixin, TemplateView):
    template_name = "main/about.html"
    page_model = AboutPage

    # Adds the About us page title and text to the context.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_page()
        context["title"] = page.title
        context["content"] = page.content
        context["text_on_page"] = page.text_on_page
        return context


# View for pages that are not ready yet; shows the 404 page for them.
class PageNotFoundView(TemplateView):
    template_name = "404.html"
    extra_context = {"title": NOT_FOUND_TITLE}

    # Returns the 404 page with the matching HTTP status.
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs), status=404)


# 404 handler for all unknown URLs when DEBUG = False.
def page_not_found(request, exception):
    return render(request, "404.html", {"title": NOT_FOUND_TITLE}, status=404)
