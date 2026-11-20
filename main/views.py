from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'main/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная страница'
        context['content'] = 'Добро пожаловать на главную страницу сайта Home'
        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home -  О нас'
        context['content'] = 'О нас'
        context['text_on_page'] = 'Мы - команда профессионалов, которая занимается разработкой и продажей мебели.'
        return context  

# def about(request):
#     content = {
#         "title": "Home -  О нас",
#         "content": "О нас",
#         "text_on_page": "Мы - команда профессионалов, которая занимается разработкой и продажей мебели.",
#     }
#     return render(request, "main/about.html", content)
