from django.contrib import admin

# Register your models here.
from blog.models import Article

admin.site.register(Article)