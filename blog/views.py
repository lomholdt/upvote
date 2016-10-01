from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.timezone import now

from blog.models import Article, Vote


def index(request):
    articles = Article.objects.filter(published_at__lte=now()).order_by('-rank')
    latest_articles = Article.objects.filter(published_at__lte=now()).order_by('-created')[3:]
    context = {'articles': articles, 'latest_articles': latest_articles}
    return render(request, 'blog/index.html', context=context)


def view(request, slug):
    article = Article.objects.get(slug=slug)

    # upvotes = Vote.objects.filter(article=article, direction__exact=1).count()
    # downvotes = Vote.objects.filter(article=article, direction__exact=0).count()
    # article.downs = downvotes
    # article.ups = upvotes
    article.set_rank()
    context = {'article': article}
    return render(request, 'blog/view.html', context=context)


def vote(request, article, direction, identification):
    article = Article.objects.get(pk=article)
    vote, bool = Vote.objects.update_or_create(article=article, identification=identification, defaults={'direction': direction})
    return JsonResponse(bool, safe=False)

