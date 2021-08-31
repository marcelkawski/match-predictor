from django.views import generic
from collections import defaultdict
import datetime

from games.models import Game
from leagues.models import League


class ListGameView(generic.ListView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        leagues_games = {}
        leagues = League.objects.all()
        for league in leagues:
            games_gr_by_date = defaultdict(list)
            games = Game.objects.filter(season__is_active=True,
                                        season__league=league,
                                        date__gte=datetime.date.today()).order_by('date')
            for game in games:
                games_gr_by_date[game.date.date()].append(game)
            leagues_games[league] = dict(games_gr_by_date)
        context['leagues_games'] = leagues_games
        return context
