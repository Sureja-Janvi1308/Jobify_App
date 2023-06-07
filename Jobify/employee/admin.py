from django.contrib import admin
from employee.models import *

# Register your models here.
admin.site.register(EmployeeProfile)
admin.site.register(Employee)
admin.site.register(Applied_Jobs)