from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.contrib import messages

from employee.models import EmployeeProfile


def user_is_employer(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_employer:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_employee(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_employee:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def profile_created(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        try:
            employeeprofile = user.employeeprofile
        except EmployeeProfile.DoesNotExist:
            messages.error(request, f'Please Create Employee Profile First')
            return render(request, 'error.html')

    return wrap
