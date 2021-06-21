from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from accounts.models import User
from accounts.forms import CreateUserForm


# models tests

class UserTest(TestCase):

    def create_user(self, username='test_username', email='test_email@gmail.com'):
        return User.objects.create(username=username, email=email)

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), user.username)


# views tests

class SignUpViewTests(TestCase):

    def test_status_code(self):
        response = self.client.get('/accounts/signup/')
        self.assertEquals(response.status_code, 200)

    def test_form(self):
        user_data = {'username': 'test_user',
                     'email': 'test_email@gmail.com',
                     'password1': 'test_pwd123',
                     'password2': 'test_pwd123'}
        response = self.client.post("/accounts/signup/", data=user_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'accounts/registration_email.html')
        self.assertTemplateUsed(response, 'accounts/conf_email_info.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_invalid_form(self):
        user_data = {'username': 'test_user',
                     'email': 'test_email.com',
                     'password1': 'test',
                     'password2': 'test_pwd'}
        response = self.client.post("/accounts/signup/", data=user_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'accounts/signup.html')


    def test_view_url_by_name(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertTemplateUsed(response, 'base.html')
