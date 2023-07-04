from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('dashboard',DashboardView.as_view(), name='dashboard' ),
    path('employer-profilecreate/', EmployerProfileCreateView.as_view(), name='employer-profile-create'),
    path('employer-profileview/', EmployerProfileView.as_view(), name='employer-profile-view'),
    path('employer-profileupdate/', EmployerProfileUpdateView.as_view(), name='employer-profile-update'),
    path('employer-profiledelete/', EmployerProfileDeleteView.as_view(), name='employer-profile-delete'),
    path('job-create/', JobCreateView.as_view(), name='employer-job-create'),
    path('mark-active/<int:job_id>/', JobActive.as_view(), name='active'),
    path('update-job/<int:job_id>/', JobUpdateView.as_view(), name='employer-job-update'),
    path('delete-job/<int:job_id>/', JobDeleteView.as_view(), name='employer-job-delete'),
    path('jobs', JobListView.as_view(), name='jobs'),
    path('applicants/<int:job_id>/', ApplicantPerJobView.as_view(), name='applicants-view'),
    path('all-applicants/', ApplicantsListView.as_view(), name='all-applicant'),
    path('payment/', Payments, name='payment'),
    path('wallet/', WalletView.as_view(), name='wallet'),

    path('paymenthandler/', csrf_exempt(PaymentHandlerView.as_view()), name='paymenthandler'),
    path('mark-select/<int:applicant_id>/', ApplicantSelectionView.as_view(), name='select'),





]