from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
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


@receiver(post_save, sender=Applicants)
def deduct_balance(sender, instance, created, **kwargs):
    if not created and instance.is_selected:
        wallet = Wallet.objects.get(company=instance.job.user.employerprofile)
        if wallet.balance >= 3:
            wallet.balance -= 3
            wallet.save()
    # if instance.view_resume:
    #     wallet = Wallet.objects.get(user=instance.job.user)
    #     if wallet.balance >= 5:
    #         wallet.balance -= 5
    #         wallet.save()
    # if instance.EmployeeProfile:
    #     wallet = Wallet.objects.get(user=instance.job.user)
    #     if wallet.balance >= 10:
    #         wallet.balance -= 10
    #         wallet.save()
