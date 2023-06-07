from django.contrib import admin

from company.models import *

# Register your models here.

admin.site.register(EmployerProfile)
admin.site.register(Job)
admin.site.register(Applicants)
