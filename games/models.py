from django.db import models
from clubs.models import Club


class Game(models.Model):
    home_team = models.ForeignKey(Club, related_name='home_team_games', on_delete=models.CASCADE)
    visiting_team = models.ForeignKey(Club, related_name='visiting_team_games', on_delete=models.CASCADE)
    date = models.DateTimeField()
    home_team_goals = models.PositiveIntegerField()
    visiting_team_goals = models.PositiveIntegerField()
