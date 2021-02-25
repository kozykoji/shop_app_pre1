from django.db import models
from django.core.validators import URLValidator
from django.urls import reverse
from django.utils import timezone

# Create your models here.

GENRE_CHOICES = (
    ('メンズ', 'メンズ'),
    ('ウィメンズ', 'ウィメンズ'),
    ('メンズ・ウィメンズ', 'メンズ・ウィメンズ'),
)
TREAT_USED_CHOICES = (
    ('有','有'),
    ('無','無'),
)

class Brand(models.Model):
    brandname = models.CharField('ブランド名', max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.brandname 

class List(models.Model):
    shopname = models.CharField('店名',max_length=200)
    treatbrands = models.ManyToManyField(Brand, '取扱ブランド')
    treatused = models.CharField('古着の取扱',max_length=200, choices=TREAT_USED_CHOICES)
    genre =  models.CharField('ジャンル',max_length=200, choices=GENRE_CHOICES)
    address = models.CharField('所在地',max_length=200)
    hpurl = models.TextField('ホームページURL',validators=[URLValidator()], blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shopname 