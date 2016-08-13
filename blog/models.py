import os
from uuid import uuid4


from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify
from redactor.fields import RedactorField
from django.utils.translation import ugettext as _

# Create your models here.
from news import settings


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name=_('Titel'))
    lead = models.CharField(max_length=512, verbose_name=_('Manchet'))
    body = RedactorField(verbose_name=_('Tekst'))
    cover_photo = models.ImageField(blank=True, null=True, upload_to=PathAndRename('cover-photos'))
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    published_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_cover_photo(self):
        if self.cover_photo:
            return
            # return os.path.join(settings.STATIC_URL, self.cover_photo)