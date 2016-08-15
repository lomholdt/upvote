import itertools
from django import forms
from django.utils.text import slugify

from blog.models import Article


class ArticleCreateForm(forms.ModelForm):
    def save(self, **kwargs):
        instance = super(ArticleCreateForm, self).save(commit=False)
        instance.rank = instance.get_rank()
        max_length = Article._meta.get_field('slug').max_length
        instance.slug = orig = slugify(instance.title)[:max_length]

        for x in itertools.count(1):
            if not Article.objects.filter(slug=instance.slug).exists():
                break
            # Truncate the original slug dynamically. Minus 1 for the hyphen.
            instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        instance.save()
        return instance
