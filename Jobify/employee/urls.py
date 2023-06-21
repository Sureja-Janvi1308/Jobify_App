from django.urls import path

from employee.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='Homepage'),
    path('employee/profileview/', EmployeeProfileView.as_view(), name='employee-profile-view'),
    path('employee/profilecreate/', EmployeeProfileCreateView.as_view(), name='employee-profile-create'),
    path('employee/profileupdate/', EmployeeProfileUpdateView.as_view(), name='employee-profile-update'),
    path('employee/profiledelete/', EmployeeProfileDeleteView.as_view(), name='employee-profile-delete'),
    path('employee/jobsearch/', SearchView.as_view(), name='search-job'),
    path('employee/educationdetails/', EducationCreateView.as_view(), name='employee-edu-profile'),
    path('employee/experiencedetails/', ExperienceCreateView.as_view(), name='employee-exp-profile'),
    path('employee/skillsdetails/', SkillCreateView.as_view(), name='employee-skill-profile'),
    path('jobdetails/<int:job_id>/', JobDetailView.as_view(), name='job-detail'),
    path('applyjob/<int:job_id>/', ApplyJobView.as_view(), name='apply-job'),
    path('resumepreview/', GenerateResumeView.as_view(), name='resume-preview'),
    path('resumedownload/', DownloadResumeView.as_view(), name='resume-download'),




]
