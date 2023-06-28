from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from Jobify.settings import DEFAULT_FROM_EMAIL
from company.models import Applicants


@receiver(post_save, sender=Applicants)
def send_application(sender, instance, created, **kwargs):
    if created:
        job = instance.job
        job_title = instance.job.title
        applicant_name = instance.applicant.first_name + ' ' + instance.applicant.last_name
        employer_email = instance.job.user.email
        subject = 'New Job Application for { job_title }'
        context = {
            'job_title': job_title,
            'applicant_name': applicant_name
        }
        message = f'Hello, \n\nA new Application has been received  for the position of {job_title}\n\nApplicant : {applicant_name}'
        from_email = DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [employer_email])
