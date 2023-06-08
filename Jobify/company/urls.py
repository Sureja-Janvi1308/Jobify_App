from django.urls import path
from .views import *

urlpatterns = [
    path('employer/profile/create/', EmployerProfileCreateView.as_view(), name='employer-profile-create'),
    path('employer/profile/view/<int:pk>', EmployerProfileView.as_view(), name='employer-profile-view'),



]