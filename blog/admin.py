from django.contrib import admin

# Register your models here.
from blog.forms import ArticleCreateForm
from blog.models import Article


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleCreateForm
    readonly_fields = ('ups', 'downs', 'rank')


admin.site.register(Article, ArticleAdmin)