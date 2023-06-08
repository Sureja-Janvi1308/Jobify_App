from django.urls import path

from employee.views import *
urlpatterns= [
    path('employee/profile/view/', EmployeeProfileView.as_view(), name='employee-profile-view'),
    path('employee/profile/create/', EmployeeProfileCreateView.as_view(), name='employee-profile-create'),
    path('employee/profile/update/<int:pk>/', EmployeeProfileUpdateView.as_view(), name='employee-profile-update'),
    path('employee/profile/delete/<int:pk>/', EmployeeProfileDeleteView.as_view(), name = 'employee-profile-delete')

]

