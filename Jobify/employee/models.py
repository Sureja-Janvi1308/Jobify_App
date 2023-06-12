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


class Employee(models.Model):
    CHOICES = (
        ('full time', 'Full Time'),
        ('part time', 'Part Time'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )
    user = models.ForeignKey(EmployeeProfile, related_name='employee' ,on_delete=models.CASCADE, null=True)
    education = models.CharField(max_length=200, null=True, blank=False)
    grad_year = models.IntegerField(blank=True)
    skills = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    job_type = models.CharField(choices=CHOICES, default='', max_length=100)
    # company = models.ForeignKey(Job, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Applied_Jobs(models.Model):
    job = models.ForeignKey(Job, related_name='applied_jobs', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    is_saved = models.BooleanField(default=False)

    def __str__(self):
        return self.job.title

# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     contact_number = models.CharField(max_length=20)
#     date_of_birth = models.DateField()
#     address = models.CharField(max_length=200)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
#
#     class Meta:
#         abstract = True
#
#
# class TimeStamped(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True
#
#
# class Education(TimeStamped):
#     candidate = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     institution_name = models.CharField(max_length=100)
#     degree = models.CharField(max_length=100)
#     field_of_study = models.CharField(max_length=100)
#     start_date = models.DateField()
#     end_date = models.DateField()
#
#
# class Experience(TimeStamped):
#     candidate = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=100)
#     job_title = models.CharField(max_length=100)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     description = models.TextField()
#
#
# class Skill(TimeStamped):
#     candidate = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     years_of_experience = models.IntegerField()

#
# class Resume(TimeStamped):
#     candidate = models.OneToOneField('UserProfile', on_delete=models.CASCADE)
#     file = models.FileField(upload_to='resumes/')
#     summary = models.TextField()
#
#
# class JobApplication(TimeStamped):
#     candidate = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     job_listing = models.ForeignKey(Job, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20)
#
#
#
#
#
