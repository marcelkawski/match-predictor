import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchpredictor.settings')
django.setup()
import datetime

from games.models import Game
from nn.predict import predict_match
from utils.fake_data import fake_date


if __name__ == '__main__':
    today = fake_date  # just to predict matches during the season break
    delta = datetime.timedelta(days=7)
    date_limit = today + delta
    games = Game.objects.filter(season__is_active=True,
                                date__gte=today,
                                date__lte=date_limit)
    for game in games:
        ht_chances, draw_chances, at_chances = predict_match(game.season.league.name,
                                                             game.home_team.ss_name,
                                                             game.visiting_team.ss_name)
        game.ht_chances = float(ht_chances)
        game.draw_chances = float(draw_chances)
        game.at_chances = float(at_chances)
        game.save()

    print('All following games predicted!')
