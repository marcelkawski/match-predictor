from django.test import TestCase
from accounts.models import User


class UserTest(TestCase):

    # models tests

    def create_user(self, username='test_username', email='test_email@gmail.com'):
        return User.objects.create(username=username, email=email)

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), user.username)
