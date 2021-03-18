from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Club(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    crest = models.ImageField(upload_to='crests', blank=True, null=True)
    fans = models.ManyToManyField(User, through='ClubFan')


class ClubFan(models.Model):
    user = models.ForeignKey(User, related_name='user_clubs', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, related_name='club_fans', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'club')
