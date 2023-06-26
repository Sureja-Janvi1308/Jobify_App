from io import BytesIO
from xhtml2pdf import pisa

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView, ListView, FormView, TemplateView
from django.views.generic.edit import UpdateView
from django.forms import modelformset_factory
from authentication.models import CustomUser
from company.forms import ApplyJobForm
from company.models import Job, EmployerProfile, Applicants
from employee.forms import EmployeeProfileForm, EducationForm, ExperienceForm, SkillForm, ExperienceFormSet, \
    EducationFormSet
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
        educations = Education.objects.filter(user=self.request.user)
        context['educations'] = educations
        experiences = Experience.objects.filter(user=self.request.user)
        context['experiences'] = experiences
        skills = Skill.objects.filter(user=self.request.user)
        context['skills'] = skills

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
        messages.success(self.request, "Your Profile was updated successfully.")
        return super(EmployeeProfileUpdateView, self).form_valid(form)


class EmployeeProfileDeleteView(DeleteView):
    template_name = 'Accounts/employee/view_profile.html'
    success_url = reverse_lazy('Homepage')
    success_message = 'Profile Deleted Successfully'

    def get_object(self, queryset=None):
        return self.request.user.employeeprofile

    def form_valid(self, form):
        return super().form_valid(form)


class EducationCreateView(CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'Accounts/employee/create-education.html'
    success_url = reverse_lazy('employee-exp-profile')

    def get_context_data(self, **kwargs):

        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['formset'] = EducationFormSet(self.request.POST, prefix='education')

        else:
            data['formset'] = EducationFormSet(queryset=Education.objects.none())
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

            return super(EducationCreateView, self).form_valid(form)
        else:
            return super().form_invalid(form)


# class EducationUpdateView(UpdateView):
#     model = Education
#     fields = ['degree']
#
#     template_name = 'Accounts/employee/update_education.html'
#     success_url = reverse_lazy('employee-profile-view')
#
#
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         if self.request.POST:
#
#             data['formset'] = EducationFormSet(self.request.POST)
#         else:
#             data['formset'] = EducationFormSet()
#         return data
#
#
#
#     def form_valid(self, form):
#         print('fndjsnujn')
#         context = self.get_context_data()
#         formset = context['formset']
#
#         if formset.is_valid():
#             formset.save()
#             messages.success(self.request, "Your Profile was updated successfully.")
#             return super().form_valid(form)
#         else:
#             for form_errors in formset.errors:
#                 for field_errors in form_errors:
#                     for error in field_errors:
#                         print(f'Formset errors :{error}')
#             return self.form_invalid(form)
#
#     def form_invalid(self, form):
#         print(form.errors)
#         return form


class EducationUpdateView(UpdateView):
    model = Education
    form_class = EducationForm

    template_name = 'Accounts/employee/update_education.html'
    success_url = reverse_lazy('employee-profile-view')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = EducationFormSet(self.request.POST)
        else:
            data['formset'] = EducationFormSet()
        return data

    def form_valid(self, form):

        formset = EducationFormSet(self.request.POST, queryset=Education.objects.filter(user=self.request.user))
        if formset.is_valid():

            form.instance.user = self.request.user
            self.object = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = self.request.user
                instance.save()
            messages.success(self.request, "Your Profile was updated successfully.")

    def form_invalid(self, form):
        print(form)
        return form


#


class EducationDeleteView(DeleteView):
    template_name = 'Accounts/employee/view_profile.html'
    success_url = reverse_lazy('Homepage')

    def get_object(self, queryset=None):
        return self.request.user.educations.all().first()

    def form_valid(self, form):
        formset = modelformset_factory(Education, form=EducationForm)
        messages.success(self.request, f'Profile Deleted Successfully')
        return super(EducationDeleteView, self).form_valid(form)


class ExperienceCreateView(CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'Accounts/employee/create-experience.html'
    success_url = reverse_lazy('employee-skill-profile')
    success_message = 'Experience Profile Created Successfully'

    def get_context_data(self, **kwargs):

        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['formset'] = ExperienceFormSet(self.request.POST)

        else:
            data['formset'] = ExperienceFormSet(queryset=Experience.objects.none())
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

            return super(ExperienceCreateView, self).form_valid(form)
        else:
            return super().form_invalid(form)


class ExperienceDeleteView(DeleteView):
    template_name = 'Accounts/employee/view_profile.html'
    success_url = reverse_lazy('Homepage')

    def get_object(self, queryset=None):
        return self.request.user.experiences.all().first()

    def form_valid(self, form):
        formset = modelformset_factory(Experience, form=ExperienceForm)
        messages.success(self.request, f'Profile Deleted Successfully')
        return super(ExperienceDeleteView, self).form_valid(form)


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
            data['formset'] = SkillFormSet(queryset=Skill.objects.none())
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

            return super(SkillCreateView, self).form_valid(form)
        else:
            return super().form_invalid(form)


SkillFormSet = modelformset_factory(Skill, form=SkillForm, extra=0)


class SkillDeleteView(DeleteView):
    template_name = 'Accounts/employee/view_profile.html'
    success_url = reverse_lazy('Homepage')

    def get_object(self, queryset=None):
        return self.request.user.skills.all().first()

    def form_valid(self, form):
        formset = modelformset_factory(Skill, form=SkillForm)
        messages.success(self.request, f'Profile Deleted Successfully')
        return super(SkillDeleteView, self).form_valid(form)


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
        applicant = form.save(commit=False)
        applicant.applicant = self.request.user
        applicant.save()

        return self.form_valid(form)


class GenerateResumeView(View):
    def get(self, request):
        user = self.request.user
        employee_profile = EmployeeProfile.objects.get(user=user)
        educations = Education.objects.filter(user=user)
        experiences = Experience.objects.filter(user=user)
        skills = Skill.objects.filter(user=user)

        template = get_template('Accounts/employee/resume.html')
        context = {
            'employee_profile': employee_profile,
            'educations': educations,
            'experiences': experiences,
            'skills': skills

        }
        rendered_template = template.render(context)
        return render(request, 'Accounts/employee/resume_preview.html', {'rendered_template': rendered_template})


class DownloadResumeView(View):
    def get(self, request):
        user = self.request.user
        employee_profile = EmployeeProfile.objects.get(user=user)
        educations = Education.objects.filter(user=user)
        experiences = Experience.objects.filter(user=user)
        skills = Skill.objects.filter(user=user)

        template = get_template('Accounts/employee/resume.html')
        context = {
            'employee_profile': employee_profile,
            'educations': educations,
            'experiences': experiences,
            'skills': skills

        }
        rendered_template = template.render(context)
        pdf_file = BytesIO()
        pisa.CreatePDF(BytesIO(rendered_template.encode('utf-8')), pdf_file)

        response = HttpResponse(content_type='application/pdf')
        response['content-Disposition'] = 'attachment; filename="resume.pdf"'
        response.write(pdf_file.getvalue())
        return response
