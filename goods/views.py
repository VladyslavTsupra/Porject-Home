

from django.http import Http404
from django.views.generic import DetailView, ListView

from goods.models import Products
from goods.utils import q_search


# Контролер каталогу товарів з фільтрацією, сортуванням і пошуком.
class CatalogView(ListView):
    model = Products
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'
    paginate_by = 3
    allow_empty = False
    
    
    # Повертає товари за категорією чи пошуковим запитом з урахуванням фільтрів.
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")
        
        if category_slug == "all":
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != "default":
            goods = goods.order_by(order_by)
            
        return goods
   
    # Додає в контекст заголовок і slug категорії.
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'HOME - Каталог'
        context['slug_url'] = self.kwargs.get('category_slug')
        return context

# Контролер сторінки окремого товару.
class ProductView(DetailView):

    template_name = 'goods/product.html'
    slug_url_kwarg = "product_slug"
    context_object_name = 'product'
    
    # Повертає товар за slug з URL.
    def get_object(self, queryset = None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product 
    
    # Додає в контекст назву товару як заголовок.
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

