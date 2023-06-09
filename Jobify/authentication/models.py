from django.db import models
from django.utils import timezone
from phone_field import PhoneField
from django_countries.fields import CountryField

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.conf import settings




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('User must have Email Address')
        email = self.normalize_email(email)
        user = self.model(email=email, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')

    )
    email = models.EmailField(_('email address'), unique=True, max_length=100,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    is_employee = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    gender = models.CharField(choices=GENDER, default='', max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + "   " + self.last_name

    objects = CustomUserManager()
