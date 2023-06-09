from django.urls import path
from .views import *

urlpatterns = [
    path('employer/profile/create/', EmployerProfileCreateView.as_view(), name='employer-profile-create'),
    path('employer/profile/view/', EmployerProfileView.as_view(), name='employer-profile-view'),
    path('employer/profile/update/', EmployerProfileUpdateView.as_view(), name='employer-profile-update'),
    path('employer/profile/delete/', EmployerProfileDeleteView.as_view(), name='employer-profile-delete'),




]