from django.db import models
from clubs.models import Club
from seasons.models import Season


class Game(models.Model):
    home_team = models.ForeignKey(Club, related_name='home_team_games', on_delete=models.CASCADE)
    visiting_team = models.ForeignKey(Club, related_name='visiting_team_games', on_delete=models.CASCADE)
    date = models.DateTimeField()
    ht_chances = models.FloatField(null=True, default=None)
    draw_chances = models.FloatField(null=True, default=None)
    at_chances = models.FloatField(null=True, default=None)
    season = models.ForeignKey(Season, blank=True, related_name='season_games', on_delete=models.CASCADE)

    def __str__(self):
        return self.home_team.name + '-' + self.visiting_team.name + str(self.season.id)
