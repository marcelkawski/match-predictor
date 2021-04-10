from django.contrib import auth
from clubs.models import Club


auth.models.User._meta.get_field('email')._unique = True


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return self.username
