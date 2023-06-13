from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

from django.utils import timezone
from django.db import models
from django_countries.fields import CountryField
from phone_field import PhoneField

from Jobify import settings
from company.models import Job


# Create your models here.


class EmployeeProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='employeeprofile',  null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=False)
    email = models.EmailField(default='')
    phone_number = models.CharField(max_length=17, blank=True)
    address_1 = models.CharField(_("address"), max_length=128)
    address_2 = models.CharField(_("address contd"), max_length=128, blank=True)
    city = models.CharField(_("city"), max_length=64)
    state = models.CharField(_("state"), )
    pincode = models.CharField(_("zip code"), max_length=6)
    country = CountryField()
    profile_pic = models.ImageField(upload_to='images/', max_length=100, default='')

    def __str__(self):
        return self.first_name + self.last_name

    class Meta:
        verbose_name = 'employeeprofile'



    def __str__(self):
        return self.user


class Applied_Jobs(models.Model):
    job = models.ForeignKey(Job, related_name='applied_jobs', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    is_saved = models.BooleanField(default=False)

    def __str__(self):
        return self.job.title




class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Education(TimeStamped):
    user = models.ForeignKey(EmployeeProfile, related_name='educations' , on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()


class Experience(TimeStamped):
    user = models.ForeignKey(EmployeeProfile,related_name='experiences', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()


class Skill(TimeStamped):
    user = models.ForeignKey(EmployeeProfile,related_name='skills',  on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()


