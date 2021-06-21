from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from games.models import Game
from clubs.models import Club
from leagues.models import League
from seasons.models import Season


class GamesTests(TestCase):

    def setUp(self):
        league = League.objects.create(name='Test League')
        season = Season.objects.create(league=league, api_id=0)
        home_team = Club.objects.create(name='Club A')
        visiting_team = Club.objects.create(name='Club B')
        Game.objects.create(home_team=home_team,
                            visiting_team=visiting_team,
                            date=timezone.now(),
                            season=season)

    def test_game_content(self):
        home_team = Club.objects.get(name='Club A')
        visiting_team = Club.objects.get(name='Club B')
        league = League.objects.get(name='Test League')
        season = Season.objects.get(league=league)
        game = Game.objects.get(id=1)
        self.assertEquals(game.home_team, home_team)
        self.assertEquals(game.visiting_team, visiting_team)
        self.assertEquals(game.season, season)


    def test_game_creation(self):
        game = Game.objects.get(id=1)
        self.assertTrue(isinstance(game, Game))
        self.assertEqual(game.__str__(), game.home_team.name + '-' + game.visiting_team.name + str(game.season.id))
