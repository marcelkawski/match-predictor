from django.test import TestCase
from leagues.models import League


class LeagueTest(TestCase):

    # models tests

    def create_league(self, name='Test League'):
        return League.objects.create(name=name)

    def test_league_creation(self):
        league = self.create_league()
        self.assertTrue(isinstance(league, League))
        self.assertEqual(league.__str__(), league.name)
