from django.contrib import admin
from employee.models import *

# Register your models here.
admin.site.register(EmployeeProfile)
admin.site.register(Education)
admin.site.register(Applied_Jobs)
admin.site.register(Skill)
admin.site.register(Experience)