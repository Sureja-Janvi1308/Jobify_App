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

