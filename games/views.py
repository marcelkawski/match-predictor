from django.views import generic
from games.models import Game
from collections import defaultdict
import datetime


class ListGameView(generic.ListView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games_gr_by_date = defaultdict(list)
        games = Game.objects.filter(date__gte=datetime.date.today()) \
            .order_by('date')
        for game in games:
            games_gr_by_date[game.date.date()].append(game)
        context['games_gr_by_dat'] = dict(games_gr_by_date)
        return context
