from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.contrib import messages

from company.models import EmployerProfile
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

#
# def profile_created(function):
#     def wrap(request, *args, **kwargs):
#         user = request.user
#         try:
#             employeeprofile = user.employeeprofile
#             return function(request, *args, **kwargs)
#         except EmployeeProfile.DoesNotExist:
#             messages.error(request, f'Please Create Employee Profile First')
#             return render(request, 'error.html')
#
#     return wrap


def profile_created(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_employee:

            try:
                employeeprofile = user.employeeprofile
                return function(request, *args, **kwargs)
            except EmployeeProfile.DoesNotExist:
                messages.error(request, f'Please Create Employee Profile First')
                return render(request, 'error.html')

        else:
            try:
                employerprofile = user.employerprofile
                return function(request, *args, **kwargs)
            except EmployerProfile.DoesNotExist:
                messages.error(request, f'Please Create Employer Profile First')
                return render(request, 'error.html')

    return wrap
