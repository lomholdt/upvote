from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^artikel/(?P<slug>[\w-]+)$', views.view, name='article_view'),
]
