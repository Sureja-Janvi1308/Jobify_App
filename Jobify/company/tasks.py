from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from Jobify.settings import DEFAULT_FROM_EMAIL
from company.models import Applicants


@shared_task
def send_selected_email_task(applicant_id):
    users = Applicants.objects.get(id=applicant_id)

    subject = 'Congratulations! You have been selected!'
    message = f'Dear,\n\n' \
              f'Congratulations! Your profile has been selected for a {users.job.title}\n' \
              f'We appreciate your interest and look forward to working with you.\n\n' \
              f'Please do checkout our Company"s Website {users.job.user.employerprofile.website} \n' \
              f'Best regards, \n' \
              f'{users.job.user.employerprofile.company_name}'

    from_email = DEFAULT_FROM_EMAIL
    to_email = users.applicant.email
    send_mail(subject, message, from_email, [to_email])



