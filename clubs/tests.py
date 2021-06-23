from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.messages import get_messages
from http import HTTPStatus

from clubs.models import Club, ClubFan
from accounts.models import User


# models tests

class ClubTest(TestCase):

    def create_club(self, name='Test Club'):
        return Club.objects.create(name=name)

    def test_club_creation(self):
        club = self.create_club()
        self.assertTrue(isinstance(club, Club))
        self.assertEqual(club.__str__(), club.name)


class ClubFanTest(TestCase):

    def create_clubfan(self, username='test_username', email='test_email@gmail.com'):
        user = User.objects.create(username='test_user', email='test_email@gmail.com')
        club = Club.objects.create(name='Test Club')
        return ClubFan.objects.create(user=user, club=club)

    def test_clubfan_creation(self):
        clubfan = self.create_clubfan()
        self.assertTrue(isinstance(clubfan, ClubFan))
        self.assertEqual(clubfan.__str__(), clubfan.user.username + '-' + clubfan.club.name)


# views tests

class ClubsRankingViewTests(TestCase):

    def setUp(self):
        club1 = Club.objects.create(name='Club A')
        club2 = Club.objects.create(name='Club B')
        club3 = Club.objects.create(name='Club C')
        club4 = Club.objects.create(name='Club D')

        user1 = User.objects.create(username='test_user1', email='test_email1@gmail.com')
        user2 = User.objects.create(username='test_user2', email='test_email2@gmail.com')
        user3 = User.objects.create(username='test_user3', email='test_email3@gmail.com')

        # club1
        ClubFan.objects.create(user=user1, club=club1)

        # club2
        ClubFan.objects.create(user=user1, club=club2)
        ClubFan.objects.create(user=user2, club=club2)

        # club4
        ClubFan.objects.create(user=user1, club=club4)
        ClubFan.objects.create(user=user2, club=club4)

        # club3
        ClubFan.objects.create(user=user1, club=club3)
        ClubFan.objects.create(user=user2, club=club3)
        ClubFan.objects.create(user=user3, club=club3)

    def test_status_code(self):
        response = self.client.get('/clubs/clubs-ranking/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('clubs:clubs_ranking'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('clubs:clubs_ranking'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clubs/clubs_ranking.html')
        self.assertTemplateUsed(response, 'clubs/club_base.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_ListGameView_context(self):
        response = self.client.get(reverse('clubs:clubs_ranking'))
        clubs_ranking = response.context['clubs_ranking']
        clubs = Club.objects.all()
        self.assertEquals(len(clubs_ranking), 3)
        self.assertEquals(clubs_ranking[1], [clubs[2]])
        self.assertEquals(clubs_ranking[2], [clubs[1], clubs[3]])
        self.assertEquals(clubs_ranking[3], [clubs[0]])


class AddClubToFavsViewTests(TestCase):

    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='test_user')[0])
        Club.objects.create(name='Club A')

    def test_status_code(self):
        club = Club.objects.get(pk=1)
        response = self.client.get(f'/clubs/add-to-favs/{club.slug}/')
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_view_url_by_name(self):
        club = Club.objects.get(pk=1)
        response = self.client.get(reverse('clubs:add_club_to_favs', kwargs={'slug': club.slug}))
        self.assertEquals(response.status_code, HTTPStatus.FOUND)


class AddClubToFavsViewTransactionsTests(TransactionTestCase):

    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='test_user')[0])
        Club.objects.create(name='Club A')

    def test_IntegrityError(self):
        user = User.objects.get(pk=1)
        club = Club.objects.get(pk=1)
        self.client.get(reverse('clubs:add_club_to_favs', kwargs={'slug': club.slug}))
        with self.assertRaises(IntegrityError):
            ClubFan.objects.create(user=user, club=club)
        response = self.client.get(reverse('clubs:add_club_to_favs', kwargs={'slug': club.slug}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'You are already a fan of the Club A')
