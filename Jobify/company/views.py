from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, TemplateView, DetailView

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
        return super(EmployerProfileCreateView, self).form_valid(form)


    @method_decorator(login_required(login_url=reverse_lazy('loginPage')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('loginPage')
        if self.request.user.is_authenticated and self.request.user.role != 'employee':
            return reverse_lazy('loginPage')
        return super().dispatch(self.request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email
        }
        return kwargs

class EmployerProfileView(DetailView):
    model = EmployerProfile
    template_name = 'Accounts/employer/view_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_profile = EmployerProfile.objects.filter(user=self.request.user)
        breakpoint()
        context['employee_profile'] = employee_profile

        return context
