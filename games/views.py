from django.shortcuts import render
from django.views import generic
from games.models import Game


class ListGameView(generic.ListView):
    model = Game
