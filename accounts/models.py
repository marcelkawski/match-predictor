from django.db import models
from django.contrib import auth
from clubs.models import Club


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return self.username
