from django.http import HttpResponse
from django.shortcuts import render



def index(request):
    
    
    content = {
        'title': 'Home - Главная страница',
        'content': 'Добро пожаловать на главную страницу сайта Home',
    }
    return render(request, 'main/index.html',content)

def about(request):
    content = {
        'title': 'Home -  О нас',
        'content': 'О нас',
        'text_on_page': 'Мы - команда профессионалов, которая занимается разработкой и продажей мебели.',
    }
    return render(request, 'main/about.html',content)

