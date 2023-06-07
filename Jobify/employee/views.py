from django.contrib import messages
from django.views.generic import UpdateView, CreateView, DeleteView

from employee.forms import EmployeeProfileForm
from employee.models import EmployeeProfile


class EmployeeProfileCreateView(CreateView):
    model = EmployeeProfile
    form_class = EmployeeProfileForm
    template_name = 'Accounts/employee/edit_profile.html'
    success_url = '/'

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
class EmployeeProfileUpdateView(UpdateView):
    model = EmployeeProfile
    form_class = EmployeeProfileForm
    template_name = 'Accounts/employee/edit_profile.html'
    success_url = '/'

class EmployeeProfileDeleteView(DeleteView):
    model = EmployeeProfile
    template_name = 'Accounts/employee/delete_profile.html'
    success_url = 'Homepage'

    # def form_valid(self, form):
    #     messages.success(self.request, "The Profile was deleted successfully.")
    #     return super(EmployeeProfileDeleteView, self).form_valid(form)








