from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, FormView, RedirectView

from authentication.forms import EmployerRegistrationForm, EmployeeRegistrationForm, UserLoginForm
from authentication.models import CustomUser


# Create your views here.

def dashboardView(request):
    return render(request, 'base.html')


class RegisterEmployeeView(CreateView):
    model = CustomUser
    form_class = EmployeeRegistrationForm
    template_name = 'Accounts/employee/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('Homepage')
        else:
            return render(request, 'Accounts/employee/register.html', {'form': form})


class RegisterEmployerView(CreateView):
    model = CustomUser
    form_class = EmployerRegistrationForm
    template_name = 'Accounts/employer/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('dashboard')
        else:
            return render(request, 'Accounts/employer/register.html', {'form': form})


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'Accounts/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        # return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)
