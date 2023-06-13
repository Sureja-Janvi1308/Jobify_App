from django.urls import path

from employee.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='Homepage'),
    path('employee/profile/view/', EmployeeProfileView.as_view(), name='employee-profile-view'),
    path('employee/profile/create/', EmployeeProfileCreateView.as_view(), name='employee-profile-create'),
    path('employee/profile/update/', EmployeeProfileUpdateView.as_view(), name='employee-profile-update'),
    path('employee/profile/delete/', EmployeeProfileDeleteView.as_view(), name='employee-profile-delete'),



]
