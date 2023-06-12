from django.urls import path
from .views import *

urlpatterns = [
    path('employer/dashboard/',DashboardView.as_view(), name='dashboard' ),
    path('employer/profile/create/', EmployerProfileCreateView.as_view(), name='employer-profile-create'),
    path('employer/profile/view/', EmployerProfileView.as_view(), name='employer-profile-view'),
    path('employer/profile/update/', EmployerProfileUpdateView.as_view(), name='employer-profile-update'),
    path('employer/profile/delete/', EmployerProfileDeleteView.as_view(), name='employer-profile-delete'),
    path('employer/jobcreate/', JobCreateView.as_view(), name='employer-job-create'),
    path('mark-active/<int:job_id>/', JobActive.as_view(), name='active'),
    path('employer/jobedit/', JobUpdateView.as_view(), name='employer-job-update'),




]