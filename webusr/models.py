from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    userName = models.CharField(
        max_length=50, default="usrname", null=False, blank=False, unique=True
    )
    emailAddress = models.EmailField(
        max_length=50, default="email", null=False, blank=False
    )
    fullName = models.CharField(
        max_length=50, default="fullName", null=False, blank=False
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    usrCode = models.CharField(max_length=70, default="45345")
    objects = UserManager()
    USERNAME_FIELD = "userName"
    REQUIRED_FIELDS = ["emailAddress"]


class City(models.Model):
    usrCode = models.CharField(max_length=70, default="45345")
    city = models.CharField(max_length=70)
