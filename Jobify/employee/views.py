from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView, ListView, FormView, TemplateView

from authentication.models import CustomUser
from employee.forms import EmployeeProfileForm, EmployeeProfileFormContinue
from employee.models import EmployeeProfile, Employee


# class EmployeeProfileView(FormView):
#     model = EmployeeProfile
#     template_name = 'Accounts/employee/view_profile.html'
#     form_class = EmployeeProfileForm
#     success_url = reverse_lazy('employee-profile-create')
#
#     def form_valid(self, form):
#         employee_profile = form.save(commit=False)
#
#         employee_profile.user = self.request.user
#         employee_profile.save()
#         return super().form_valid(form)
#
#     # def get_form_kwargs(self):
#     #     kwargs = super().get_form_kwargs()
#     #
#     #     employee_profile = EmployeeProfile.objects.filter(user=self.request.user)
#     #     kwargs['instance'] = employee_profile
#     #     return kwargs
#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#
#         employee_profile = EmployeeProfile.objects.filter(user=self.request.user)
#         form.instance = employee_profile
#         return form
#
#
#     # def form_valid(self, form):
#     #     form.save()
#     #     return super().form_valid(form)



#         return context
class EmployeeProfileCreateView(CreateView):
    model = EmployeeProfile
    form_class = EmployeeProfileForm
    template_name = 'Accounts/employee/create_profile.html'
    success_url = reverse_lazy('employee-profile-view')

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
    template_name = 'Accounts/employee/delete_profile.html'
    success_url = reverse_lazy('loginPage')

    def get_object(self, queryset=None):
        return self.request.user.employeeprofile




# class EmployeeProfileDetailView(DetailView):
#     model = EmployeeProfile
#     template_name = 'Accounts/employee/View_profile.html'
# class EmployeeProfileCreateView(CreateView):
#     model = EmployeeProfile
#     form_class = EmployeeProfileForm
#     template_name = 'Accounts/employee/edit_profile.html'
#     success_url = '/'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['initial'] = {
#             'first_name': self.request.user.first_name,
#             'last_name': self.request.user.last_name,
#             'email': self.request.user.email
#         }
#         return kwargs
#
#
# class EmployeeProfileUpdateView(UpdateView):
#     model = EmployeeProfile
#     form_class = EmployeeProfileForm
#     template_name = 'Accounts/employee/edit_profile.html'
#     success_url = '/'
#
#
# class EmployeeProfileDeleteView(DeleteView):
#     model = EmployeeProfile
#     form_class = EmployeeProfileForm
#     template_name = 'Accounts/employee/delete_profile.html'
#     success_url = reverse_lazy('employer-profile-delete')
#
#     def form_valid(self, form):
#         messages.success(self.request, "The Profile was deleted successfully.")
#         return super(EmployeeProfileDeleteView, self).form_valid(form)
class EmployeeProfileContinue(CreateView):
    model = Employee
    form_class = EmployeeProfileFormContinue
    template_name = 'Accounts/employee/continue.html'
