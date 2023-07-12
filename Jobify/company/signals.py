from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.dispatch import Signal
from authentication.models import CustomUser
from Jobify import settings
from Jobify.settings import DEFAULT_FROM_EMAIL
from company.models import Applicants, EmployerProfile, Wallet


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


@receiver(post_save, sender=EmployerProfile)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(company=instance, balance=0.00)


enquiry_form_sent = Signal()


def send_enquiry_email(sender, user, message, **kwargs):
    send_mail(
        f'Enquiry from {user}',
        message,
        user,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )

    enquiry_form_sent.connect(send_enquiry_email)
