from django.core.exceptions import ObjectDoesNotExist
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
    article.set_rank()
    context = {'article': article}
    return render(request, 'blog/view.html', context=context)


def vote(request, article, direction, identification):
    article = Article.objects.get(pk=article)
    vote, bool = Vote.objects.update_or_create(article=article, identification=identification, defaults={'direction': direction})
    return JsonResponse(bool, safe=False)


def vote_status(request, article, identification):
    try:
        vote = Vote.objects.get(article=article, identification=identification)
        return JsonResponse(vote.direction, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse('none', safe=False)