from config.settings import AUTH_USER_MODEL
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect



class CustomUser(AbstractUser):
    pass

