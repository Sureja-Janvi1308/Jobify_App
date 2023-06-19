from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from django.utils.translation import gettext as _
from phone_field import PhoneField

from Jobify import settings


# Create your models here.

class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='employerprofile', null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=False)
    email = models.EmailField(default='', unique=True)
    company_name = models.CharField(max_length=100, null=True, blank=False)
    address_1 = models.CharField(_("address"), max_length=128)
    address_2 = models.CharField(_("address contd"), max_length=128, blank=True)
    city = models.CharField(_("city"), max_length=64)
    state = models.CharField(_("state"), )
    pincode = models.CharField(_("zip code"), max_length=6)
    country = CountryField()
    mobile = models.CharField(max_length=100, unique=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    joining_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + self.last_name

    class Meta:
        verbose_name = 'Employer Profile'


class Job(models.Model):
    CHOICES = (
        ('full time', 'Full Time'),
        ('part time', 'Part Time'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='job', default='', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    job_type = models.CharField(max_length=30, choices=CHOICES, default='', null=True)
    skills_required = models.CharField(max_length=200)
    salary = models.IntegerField(null=True)
    position = models.CharField(max_length=100)
    link = models.URLField(max_length=200, default='')
    is_active = models.BooleanField(default=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Applicants(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applied', on_delete=models.CASCADE)
    is_selected = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.applicant
