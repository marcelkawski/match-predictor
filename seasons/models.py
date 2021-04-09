from django.db import models
from leagues.models import League


class Season(models.Model):
    league = models.ForeignKey(League, related_name='league_seasons', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    api_id = models.PositiveIntegerField()

    def __str__(self):
        return self.league.name + str(self.id)
