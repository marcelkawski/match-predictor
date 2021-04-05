from django.db import models


class League(models.Model):
    name = models.CharField(max_length=64, unique=True)
    country = models.CharField(max_length=64)

    def __str__(self):
        return self.name
