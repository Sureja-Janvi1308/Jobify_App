from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView

from company.forms import EmployerProfileForm
from company.models import EmployerProfile


# Create your views here.
class EmployerProfileCreateView(CreateView):
    model = EmployerProfile
    form_class = EmployerProfileForm
    template_name = 'Accounts/employer/create_profile.html'
    success_url = reverse_lazy('employer-profile-view')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The Profile was Created successfully.")
        return super(EmployerProfileCreateView, self).form_valid(form)



    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email
        }
        return kwargs

class EmployerProfileView(TemplateView):
    template_name = 'Accounts/employer/view_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employer_profile = EmployerProfile.objects.get(user=self.request.user)
        context['employer_profile'] = employer_profile

        return context

class EmployerProfileUpdateView(UpdateView):
    model = EmployerProfile
    fields = ['mobile', 'address_1', 'address_2', 'city', 'state',
              'pincode', 'country','website']

    # form_class = EmployerProfileForm
    template_name = 'Accounts/employer/update_profile.html'
    success_url = reverse_lazy('employer-profile-view')

    def get_object(self, queryset=None):
        return self.request.user.employerprofile

    def form_valid(self, form):
        messages.success(self.request, "The profile was updated successfully.")
        return super(EmployerProfileUpdateView, self).form_valid(form)


class EmployerProfileDeleteView(DeleteView):
    model = EmployerProfile
    template_name = 'Accounts/employer/delete_profile.html'
    success_url = reverse_lazy('loginPage')

    def get_object(self, queryset=None):
        return self.request.user.employerprofile


