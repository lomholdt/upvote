import os
from uuid import uuid4


from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify
from django.utils.timezone import now, utc
from redactor.fields import RedactorField
from django.utils.translation import ugettext as _
from datetime import datetime, timedelta
from math import log

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
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    rank = models.FloatField(default=0)

    def __str__(self):
        return self.title

    def get_cover_photo(self):
        if self.cover_photo:
            return self.cover_photo.url

    def get_absolute_url(self):
        return reverse('article_view', args=[str(self.slug)])

    #  RANKING
    def __epoch_seconds(self, date):
        epoch = datetime(1970, 1, 1, tzinfo=utc)
        td = date - epoch
        return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

    def __score(self, ups, downs):
        return ups - downs

    def __hot(self, ups, downs, date):
        s = self.__score(ups, downs)
        order = log(max(abs(s), 1), 10)
        sign = 1 if s > 0 else -1 if s < 0 else 0
        seconds = self.__epoch_seconds(date) - 1134028003
        return round(sign * order + seconds / 45000, 7)

    def get_rank(self):
        return self.__hot(self.ups, self.downs, self.created)

    def set_rank(self):
        self.rank = self.get_rank()
        self.save()