from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard',DashboardView.as_view(), name='dashboard' ),
    path('employer/profilecreate/', EmployerProfileCreateView.as_view(), name='employer-profile-create'),
    path('employer/profileview/', EmployerProfileView.as_view(), name='employer-profile-view'),
    path('employer/profileupdate/', EmployerProfileUpdateView.as_view(), name='employer-profile-update'),
    path('employer/profiledelete/', EmployerProfileDeleteView.as_view(), name='employer-profile-delete'),
    path('jobcreate/', JobCreateView.as_view(), name='employer-job-create'),
    path('mark-active/<int:job_id>/', JobActive.as_view(), name='active'),
    path('updatejob/<int:job_id>/', JobUpdateView.as_view(), name='employer-job-update'),
    path('deletejob/<int:job_id>/', JobDeleteView.as_view(), name='employer-job-delete'),
    path('applicants/<int:job_id>/', ApplicantPerJobView.as_view(), name='applicants-view'),
    path('all/applicants/', ApplicantsListView.as_view(), name='all-applicant'),
    # path('employer/detailview/', JobDetailView.as_view(), name='job-detail-view')




]