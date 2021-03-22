from django.views import generic
from games.models import Game


class ListGameView(generic.ListView):
    model = Game
    # template_name = 'games/game_list.html'
