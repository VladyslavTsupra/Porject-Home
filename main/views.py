from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request):
    
    categories = Categories.objects.all()
    
    content = {
        'title': 'Home - Главная страница',
        'content': 'Добро пожаловать на главную страницу сайта Home',
        'categories': categories,
    }
    return render(request, 'main/index.html',content)

def about(request):
    content = {
        'title': 'Home -  О нас',
        'content': 'О нас',
        'text_on_page': 'Мы - команда профессионалов, которая занимается разработкой и продажей мебели.',
    }
    return render(request, 'main/about.html',content)

