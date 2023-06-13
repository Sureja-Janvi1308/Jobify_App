from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView, ListView, FormView, TemplateView

from authentication.models import CustomUser
from company.models import Job
from employee.forms import EmployeeProfileForm
from employee.models import EmployeeProfile


class HomeView(ListView):
    model = Job
    template_name = 'Accounts/employee/home.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.all()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trendings'] = self.model.objects.filter(date_posted__month=timezone.now().month)[:3]
        return context

class SearchView(ListView):
    model = Job
    template_name = 'jobs/home.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.filter(user__city__contains=self.request.GET['city'],
                                         title__contains=self.request.GET['title'])

class EmployeeProfileCreateView(CreateView):
    model = EmployeeProfile
    form_class = EmployeeProfileForm
    template_name = 'Accounts/employee/create_profile.html'
    success_url = reverse_lazy('Homepage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email
        }
        return kwargs


class EmployeeProfileView(TemplateView):
    template_name = 'Accounts/employee/view_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_profile = EmployeeProfile.objects.get(user=self.request.user)
        context['employee_profile'] = employee_profile

        return context

class EmployeeProfileUpdateView(UpdateView):
    model = EmployeeProfile
    fields = ['phone_number', 'address_1', 'address_2', 'city', 'state',
              'pincode', 'country','profile_pic']

    template_name = 'Accounts/employee/update_profile.html'
    success_url = reverse_lazy('employee-profile-view')


    def get_object(self, queryset=None):
        return self.request.user.employeeprofile

    def form_valid(self, form):
        messages.success(self.request, "The Profile was updated successfully.")
        return super(EmployeeProfileUpdateView, self).form_valid(form)


class EmployeeProfileDeleteView(DeleteView):
    model = EmployeeProfile
    template_name = 'Accounts/employee/view_profile.html'
    success_url = reverse_lazy('homepage')

    def get_object(self, queryset=None):
        return self.request.user.employeeprofile





