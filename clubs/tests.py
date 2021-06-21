from django.test import TestCase
from clubs.models import Club, ClubFan
from accounts.models import User


class ClubTest(TestCase):

    # models tests

    def create_club(self, name='Test Club'):
        return Club.objects.create(name=name)

    def test_club_creation(self):
        club = self.create_club()
        self.assertTrue(isinstance(club, Club))
        self.assertEqual(club.__str__(), club.name)


class ClubFanTest(TestCase):

    # models tests

    def create_clubfan(self, username='test_username', email='test_email@gmail.com'):
        user = User.objects.create(username='test_user', email='test_email@gmail.com')
        club = Club.objects.create(name='Test Club')
        return ClubFan.objects.create(user=user, club=club)

    def test_clubfan_creation(self):
        clubfan = self.create_clubfan()
        self.assertTrue(isinstance(clubfan, ClubFan))
        self.assertEqual(clubfan.__str__(), clubfan.user.username + '-' + clubfan.club.name)
