from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView, ListView, FormView, TemplateView
from django.forms import modelformset_factory
from authentication.models import CustomUser
from company.forms import ApplyJobForm
from company.models import Job, EmployerProfile, Applicants
from employee.forms import EmployeeProfileForm, EducationForm, ExperienceForm, SkillForm
from employee.models import EmployeeProfile, Education, Experience, Skill


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
    template_name = 'Accounts/employee/search.html'
    context_object_name = 'jobs'

    def get_queryset(self):

        querys = self.request.GET.get('s')
        query = self.request.GET.get('q')
        if query or querys:

            employer_profile = EmployerProfile.objects.filter(city__icontains=query).prefetch_related('user')
            jobs = Job.objects.filter(title__icontains=querys).prefetch_related('user__employerprofile')
            queryset = list(employer_profile) + list(jobs)
            queryset = list({obj.id: obj for obj in queryset}.values())

            # queryset = EmployerProfile.objects.filter(Q(city__icontains=query)).prefetch_related('user__job').filter(Q(user__job__title__icontains=querys)).distinct()

        else:
            queryset = EmployerProfile.objects.none()

        return queryset


class EmployeeProfileCreateView(CreateView):
    model = EmployeeProfile
    form_class = EmployeeProfileForm
    template_name = 'Accounts/employee/create_profile.html'
    success_url = reverse_lazy('employee-edu-profile')

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
              'pincode', 'country', 'profile_pic']

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


class EducationCreateView(CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'Accounts/employee/create-education.html'
    success_url = reverse_lazy('employee-exp-profile')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = EducationFormSet(self.request.POST)
        else:
            data['formset'] = EducationFormSet()
        return data

    def form_valid(self, form):
        formset = EducationFormSet(self.request.POST, queryset=Education.objects.none())
        if formset.is_valid():
            form.instance.user = self.request.user
            self.object = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = self.request.user
                instance.save()

            return redirect(self.get_success_url())
        else:
            return super().form_invalid(form)


EducationFormSet = modelformset_factory(Education, form=EducationForm, extra=0)


class ExperienceCreateView(CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'Accounts/employee/create-experience.html'
    success_url = reverse_lazy('employee-skill-profile')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ExperienceFormSet(self.request.POST)
        else:
            data['formset'] = ExperienceFormSet()
        return data

    def form_valid(self, form):
        formset = ExperienceFormSet(self.request.POST, queryset=Experience.objects.none())
        if formset.is_valid():
            form.instance.user = self.request.user
            self.object = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = self.request.user
                instance.save()

            return redirect(self.get_success_url())
        else:
            return super().form_invalid(form)


ExperienceFormSet = modelformset_factory(Experience, form=ExperienceForm, extra=0)


class SkillCreateView(CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'Accounts/employee/create-skills.html'
    success_url = reverse_lazy('employee-profile-view')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = SkillFormSet(self.request.POST)
        else:
            data['formset'] = SkillFormSet()
        return data

    def form_valid(self, form):
        formset = SkillFormSet(self.request.POST, queryset=Skill.objects.none())
        if formset.is_valid():
            form.instance.user = self.request.user
            self.object = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = self.request.user
                instance.save()

            return redirect(self.get_success_url())
        else:
            return super().form_invalid(form)


SkillFormSet = modelformset_factory(Skill, form=SkillForm, extra=0)


# class ExperienceUpdateView(UpdateView):
#     model = Experience
#     form_class = ExperienceForm
#
#     template_name = 'Accounts/employee/edit-experience.html'
#     success_url = reverse_lazy('employee-profile-view')
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         if self.request.POST:
#             data['formset'] = ExperienceFormSet(self.request.POST, instance=self.object)
#         else:
#             data['formset'] = ExperienceFormSet(instance=self.object)
#         return data
#
#     def get_object(self, queryset=None):
#         obj, created = Experience.objects.get_or_create(id=self.kwargs['exp_id'])
#         return obj
#
#     def get_context_object_name(self, obj):
#         obj['formset'] = 'formset'
#         return obj
#
#     def form_valid(self, form):
#         formset = ExperienceFormSet(self.request.POST, instance=self.object)
#         if formset.is_valid():
#             form.instance.user = self.request.user
#             self.object = form.save()
#             instances = formset.save(commit=False)
#             for instance in instances:
#                 instance.user = self.request.user
#                 instance.save()
#                 messages.success(self.request, "The Profile was updated successfully.")
#                 return redirect(self.get_success_url())
#         else:
#             return super().form_invalid(form)


class JobDetailView(DetailView):
    model = Job
    template_name = 'Accounts/employee/detail.html'
    context_object_name = 'job'

    def get_object(self, queryset=None):
        job_id = self.kwargs['job_id']

        job = get_object_or_404(Job, id=job_id)

        return job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs['job_id']

        job = get_object_or_404(Job, id=job_id)

        context['job'] = job
        return context


class ApplyJobView(CreateView):
    model = Applicants
    form_class = ApplyJobForm
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'Successfully applied for this Job')
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('Homepage'))



    def form_valid(self, form):
        applicants = Applicants.objects.filter(applicant=self.request.user.id, job_id=self.kwargs['job_id'])
        if applicants:
            messages.info(self.request, 'You have already applied for this Job')
            return HttpResponseRedirect(reverse_lazy('Homepage'))
        form.instance.applicant = self.request.user
        form.save()
        return self.form_valid(form)

