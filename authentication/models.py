from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def create_tl(self, username, email, password=None):

        user = self.create_superuser(username, email, password)
        user.is_tl = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    TEAM_OPTIONS = [('PYTHON', 'PYTHON'), ('JAVA', 'JAVA')]

    email = models.EmailField(
        max_length=255,
        unique=True, db_index=True
    )
    username = models.CharField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_tl = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    team_name = models.CharField(max_length=255, choices=TEAM_OPTIONS)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def has_perm(self, perm, obj=None):
        if obj is None:
            return True
        return self.get_user(obj.id).has_perm(perm)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'access_token': str(refresh.access_token), 'refresh_token': str(refresh),
            }
