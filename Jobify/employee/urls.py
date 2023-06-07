from django.urls import path

from employee.views import *
urlpatterns= [
    path('employee/profile/create/', EmployeeProfileCreateView.as_view(), name='employee-profile-create'),
    path('employee/profile/delete/<int:pk>/', EmployeeProfileDeleteView.as_view(), name = 'employee-profile-delete')

]

