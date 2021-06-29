from django.test import TestCase

from seasons.models import Season
from leagues.models import League


class LeagueTest(TestCase):

    # models tests

    def create_season(self, api_id=1):
        league = League.objects.create(name='Test League')
        return Season.objects.create(league=league, api_id=api_id)

    def test_season_creation(self):
        season = self.create_season()
        self.assertTrue(isinstance(season, Season))
        self.assertEqual(season.__str__(), season.league.name + str(season.id))
