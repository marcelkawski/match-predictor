from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()


class Club(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    crest = models.ImageField(upload_to='crests', blank=True, null=True)
    fans = models.ManyToManyField(User, through='ClubFan')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ClubFan(models.Model):
    user = models.ForeignKey(User, related_name='user_clubs', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, related_name='club_fans', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + '-' + self.club.name

    class Meta:
        unique_together = ('user', 'club')
