import django
import os
import sys
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchpredictor.settings')
django.setup()
import datetime
import torch
import numpy as np

from games.models import Game
from nn.train import MatchPredictor
from data_providers.nn.get_clubs_statistics import get_opponents_stats, get_match_stats, normalize_match_stats


def predict_match(league, home_team, away_team):
    home_team_stats, away_team_stats = get_opponents_stats(league, home_team, away_team)
    match_statistics, ht_matches_played, at_matches_played = get_match_stats(home_team_stats, away_team_stats)
    match_statistics = normalize_match_stats(match_statistics, ht_matches_played, at_matches_played)

    match_statistics = np.array(list(match_statistics.values()))
    match_statistics = torch.from_numpy(match_statistics)

    model = MatchPredictor().double()
    model.load_state_dict(torch.load("nn/model.pth"))
    model.eval()

    with torch.no_grad():
        pred = model(match_statistics)

    return pred


if __name__ == '__main__':
    today = datetime.date.today()
    delta = datetime.timedelta(days=14)
    date_limit = today + delta
    games = Game.objects.filter(season__is_active=True,
                                date__gte=today,
                                date__lte=date_limit)
    for game in games:
        predict_match(game.season.league.name,
                      game.home_team.source_name,
                      game.visiting_team.source_name)
        ht_chances, draw_chances, vt_chances = predict_match(game.season.league.name,
                                                             game.home_team.source_name,
                                                             game.visiting_team.source_name)
        game.ht_chances = float(ht_chances)
        game.draw_chances = float(draw_chances)
        game.vt_chances = float(vt_chances)
        game.save()

    print('All following games predicted!')
