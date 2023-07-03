from company.models import *
from django import template

register = template.Library()


@register.simple_tag(name='is_already_applied')
def is_already_applied(job, applicant):
    applied = Applicants.objects.filter(job=job, applicant=applicant)
    if applied:
        return True
    else:
        return False


@register.simple_tag(name='has_sufficient_balance')
def has_sufficient_balance(user):
    try:
        wallet = Wallet.objects.get(company__user=user)
        return wallet.balance >= 5
    except Wallet.DoesNotExist:
        return False
