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
from django.forms import modelformset_factory
from authentication.models import CustomUser
from company.forms import ApplyJobForm
from company.models import Job, EmployerProfile, Applicants
from employee.forms import EmployeeProfileForm, EducationForm, ExperienceForm, SkillForm, ExperienceFormSet
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
        messages.success(self.request, "Your Profile was updated successfully.")
        return super(EmployeeProfileUpdateView, self).form_valid(form)


class EmployeeProfileDeleteView(FormView):
    template_name = 'Accounts/employee/view_profile.html'
    success_url = reverse_lazy('Homepage')

    def get(self, request, *args, **kwargs):
        self.employeeprofileform = EmployeeProfileForm(prefix='employeeprofile')
        self.educationform = EducationForm(prefix='educations')
        self.experienceform = ExperienceForm(prefix='experiences')
        self.skillform = SkillForm(prefix='skills')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.employeeprofileform = EmployeeProfileForm(request.POST, prefix='employeeprofile')
        self.educationform = EducationForm(request.POST, prefix='educations')
        self.experienceform = ExperienceForm(request.POST, prefix='experiences')
        self.skillform = SkillForm(request.POST, prefix='skills')
        if self.employeeprofileform.is_valid() and self.educationform.is_valid() and self.experienceform.is_valid() and self.skillform:
            return self.form_valid(self.get_form())
        else:
            return self.form_invalid(form=self.get_form())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        user = self.request.user

        if self.employeeprofileform.is_valid():
            EmployeeProfile.objects.filter(user=user).delete()

        if self.educationform.is_valid():
            Education.objects.filter(user=user).delete()

        if self.experienceform.is_valid():
            Experience.objects.filter(user=user).delete()

        if self.skillform.is_valid():
            Skill.objects.filter(user=user).delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_profile'] = self.employeeprofileform
        context['educationform'] = self.educationform
        context['experienceform'] = self.experienceform
        context['skillform'] = self.skillform
        return context

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
            data['formset'] = EducationFormSet(queryset=Education.none())
        return data

    def form_valid(self, form):
        formset = EducationFormSet(self.request.POST, queryset=Education.objects.filter(user=self.request.user))
        if formset.is_valid():
            if formset.is_valid():
                form.instance.user = self.request.user
                self.object = form.save()
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.user = self.request.user
                    instance.save()
                messages.success(self.request, "Your Profile was updated successfully.")

                for deleted_form in formset.deleted_forms:
                    deleted_form.instance.delete()
                return super().form_valid(form)

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
