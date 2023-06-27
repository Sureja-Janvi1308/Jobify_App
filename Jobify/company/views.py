from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, ListView, DetailView

from company.forms import EmployerProfileForm, CreateJobForm
from company.models import EmployerProfile, Job, Applicants


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
              'pincode', 'country', 'website']

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
    template_name = 'Accounts/employer/view_profile.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        return self.request.user.employerprofile


class DashboardView(ListView):
    model = Job
    template_name = 'Accounts/employer/dashboard.html'
    context_object_name = 'jobs'

    # @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    # @method_decorator(user_is_employer)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)


class JobCreateView(CreateView):
    model = Job
    form_class = CreateJobForm
    template_name = 'Accounts/employer/create_job.html'
    extra_context = {
        'title': 'Post New Job'
    }
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class JobActive(View):

    def get(self, request, job_id=None):
        job = get_object_or_404(Job, user_id=request.user.id, id=job_id)
        job.is_active = not job.is_active
        job.save()

        return redirect('dashboard')


class JobUpdateView(UpdateView):
    model = Job
    template_name = 'Accounts/employer/job_edit.html'
    fields = ['job_type', 'skills_required', 'salary', 'position']
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        obj, created = Job.objects.get_or_create(id=self.kwargs['job_id'])
        return obj


    def form_valid(self, form):
        messages.success(self.request, "The job  was updated successfully.")
        return super(JobUpdateView, self).form_valid(form)


class JobDeleteView(DeleteView):
    model = EmployerProfile
    template_name = 'Accounts/employer/dashboard.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        obj, created = Job.objects.get_or_create(id=self.kwargs['job_id'])
        return obj


class ApplicantPerJobView(ListView):
    model = Applicants
    template_name = 'Accounts/employer/applicants.html'
    context_object_name = 'applicants'
    paginate_by = 1


    def get_queryset(self):
        return Applicants.objects.filter(job_id=self.kwargs['job_id']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context



class ApplicantsListView(ListView):
    model = Applicants
    template_name = 'Accounts/employer/all-applicants.html'
    context_object_name = 'applicants'

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(job__user_id=self.request.user.id)


class JobListView(ListView):
    model = Job
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'
    paginate_by = 5


class JobDetailsView(DetailView):
    model = Job
    template_name = 'jobs/details.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
