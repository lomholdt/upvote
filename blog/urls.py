from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='article_index'),
    url(r'^(?P<slug>[\w-]+)$', views.view, name='article_view'),
]
