from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
import datetime

from games.models import Game
from clubs.models import Club
from leagues.models import League
from seasons.models import Season


# models tests

class GamesTests(TestCase):

    def setUp(self):
        league = League.objects.create(name='Test League')
        season = Season.objects.create(league=league, api_id=0)
        home_team = Club.objects.create(name='Club A')
        visiting_team = Club.objects.create(name='Club B')
        Game.objects.create(home_team=home_team,
                            visiting_team=visiting_team,
                            date=datetime.date(2021, 6, 22),
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


# views tests

class ListGameViewTests(TestCase):
    test_date = datetime.date.today() + datetime.timedelta(days=7)

    def setUp(self):
        league = League.objects.create(name='Test League')
        season = Season.objects.create(league=league, api_id=0, is_active=True)

        home_team1 = Club.objects.create(name='Club A')
        visiting_team1 = Club.objects.create(name='Club B')
        Game.objects.create(home_team=home_team1,
                            visiting_team=visiting_team1,
                            date=self.test_date,
                            season=season)

        home_team2 = Club.objects.create(name='Club C')
        visiting_team2 = Club.objects.create(name='Club D')
        Game.objects.create(home_team=home_team2,
                            visiting_team=visiting_team2,
                            date=self.test_date,
                            season=season)

    def test_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'games/game_list.html')
        self.assertTemplateUsed(response, 'games/game_base.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_context(self):
        response = self.client.get(reverse('home'))
        active_seasons_games = response.context['leagues_games']
        clubs = Club.objects.all()
        games = Game.objects.all()
        leagues = League.objects.all()
        date = self.test_date
        self.assertEquals(len(active_seasons_games), 1)
        self.assertEquals(list(active_seasons_games.keys())[0], leagues[0])
        self.assertEquals(active_seasons_games[leagues[0]][date][0], games[0])
        self.assertEquals(active_seasons_games[leagues[0]][date][1], games[1])
        self.assertEquals(active_seasons_games[leagues[0]][date][0].home_team, clubs[0])
        self.assertEquals(active_seasons_games[leagues[0]][date][0].visiting_team, clubs[1])
        self.assertEquals(active_seasons_games[leagues[0]][date][1].home_team, clubs[2])
        self.assertEquals(active_seasons_games[leagues[0]][date][1].visiting_team, clubs[3])
