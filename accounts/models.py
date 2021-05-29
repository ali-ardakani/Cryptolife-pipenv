from config.settings import AUTH_USER_MODEL
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.http import HttpResponseRedirect
from django.urls import  reverse


class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filepath):
    return f'images/accounts/profiles/{self.pk}/{"profile.png"}'


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Meta:
        permissions = [
            ('all', 'all of the permissions')
        ]

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(verbose_name='email', max_length=100, unique=True)
    username = models.CharField(max_length=55, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(null=True, blank=True, upload_to=get_profile_image_filepath, default='images/accounts/profiles/default_image.jpg')

    objects = MyAccountManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'images/accounts/profiles/{self.pk}/'):]

    def get_absolute_url(self):
        return reverse("accounts:user_view", args=[str(self.id)])




