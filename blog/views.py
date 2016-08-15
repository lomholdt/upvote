from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from blog.models import Article


def index(request):
    articles = Article.objects.all().order_by('-rank')
    context = {'articles': articles}
    return render(request, 'blog/index.html', context=context)


def view(request, slug):
    article = Article.objects.get(slug=slug)
    context = {'article': article}
    return render(request, 'blog/view.html', context=context)