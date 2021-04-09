from django.db import models
from django.utils.text import slugify


class League(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    logo = models.ImageField(upload_to='leagues_logos', blank=True, null=True)
    country = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
