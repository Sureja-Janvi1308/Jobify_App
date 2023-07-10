from decimal import Decimal

import razorpay
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, ListView, DetailView

from Jobify import settings
from authentication.models import CustomUser
from company.forms import EmployerProfileForm, CreateJobForm
from company.models import EmployerProfile, Job, Applicants, Wallet, Payment, Transaction
from company.signals import deduct_balance
from company.tasks import send_selected_email_task


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
        if not self.request.user.is_authenticated:
            messages.error(self.request, f'Please Login or Create An Account before Posting a Job')
            return render(self.request, 'error.html')
        user = self.request.user
        try:
            employer_profile = user.employerprofile
        except EmployerProfile.DoesNotExist:
            messages.error(self.request, 'Please Create Your Profile before Posting a Job')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)


class JobActive(View):

    def get(self, request, job_id=None):
        job = get_object_or_404(Job, user_id=request.user.id, id=job_id)
        job.is_active = not job.is_active
        job.save()

        return redirect('dashboard')


class ApplicantSelectionView(View):

    def get(self, request, applicant_id=None):
        applicant = get_object_or_404(Applicants, id=applicant_id)
        wallet = Wallet.objects.get(company__user=request.user)
        if wallet.balance >= 7:


            applicant.is_selected = not applicant.is_selected
            applicant.save()
            if applicant.is_selected:
                send_selected_email_task.delay(applicant.id)

            return redirect('all-applicant')
        else:
            HttpResponse('Insufficient balance!! Please do check your Wallet')


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
        if not self.request.user.is_authenticated:
            return redirect('login')
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
        return self.model.objects.filter(job__user=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        employer_profile = user.employerprofile
        context['wallet_balance'] = employer_profile.wallets.balance
        return context


class JobListView(ListView):
    model = Job
    template_name = 'Accounts/employee/jobs.html'
    context_object_name = 'jobs'
    paginate_by = 5


class JobDetailsView(DetailView):
    model = Job
    template_name = 'Accounts/employee/details.html'
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
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


## payment view
def Payments(request):
    razorpay_client = razorpay.Client(
        auth=(settings.KEY, settings.SECRET))
    currency = 'INR'
    amount = 20000

    razorpay_order = razorpay_client.order.create({'amount': 20000, 'currency': 'INR', 'payment_capture': 1})
    razorpay_order_id = razorpay_order['id']
    callback_url = request.build_absolute_uri('/') + "paymenthandler/"

    payment = Payment.objects.create(name=request.user, amount=amount, provider_order_id=razorpay_order_id)
    payment.save()

    context = {'razorpay_order_id': razorpay_order_id, 'razorpay_merchant_key': settings.KEY,
               'razorpay_amount': amount, 'currency': currency, 'callback_url': callback_url}

    return render(request, 'Accounts/employer/payment_1.html', context=context)


class PaymentHandlerView(View):
    def verify_signature(self, response_data):
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        return client.utility.verify_payment_signature(response_data)

    def post(self, request):

        razorpay_client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        order = Payment.objects.get(provider_order_id=razorpay_order_id)

        order.payment_id = payment_id
        order.signature_id = signature
        order.save()

        wallet = Wallet.objects.get(company__user=request.user)

        if self.verify_signature(request.POST):
            order.status = 'Success'
            order.save()
            messages.success(request, f'Your payment done successfully')

            wallet.balance += Decimal(order.amount)
            wallet.save()
            messages.success(request, f'Your amount is added to wallet')

            transaction = Transaction.objects.create(wallet=wallet, amount=order.amount)
            return redirect('wallet')
        else:
            order.status = 'Failure'
            order.save()
            messages.success(request, f'Your Payment is Failed ')
            return redirect('wallet')


class WalletView(TemplateView):
    template_name = 'Accounts/employer/wallet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = Wallet.objects.get(company__user=self.request.user)
        context['wallet'] = wallet
        return context


class ViewContact(View):
    def get(self, request, applicant_id=None):
        applicant = get_object_or_404(Applicants, id=applicant_id)
        all = Applicants.objects.filter(job__user=request.user)
        wallet = Wallet.objects.get(company__user=request.user)
        transaction = Transaction.objects.filter(wallet=wallet).first()
        contact = None
        unlock = Transaction.objects.filter(wallet__company__user=request.user.id).filter(access__contains=['contact'])
        if unlock:

            contact = applicant.applicant.employeeprofile.phone_number

            return render(request, 'Accounts/employer/all-applicants.html', {'contact': contact, 'applicants': all})
        else:
            print('ff')
            if Transaction.objects.filter(access__isnull=True):
                if wallet.balance >= 5:
                    wallet.balance -= 5
                    wallet.save()
                    Transaction.objects.create(wallet=wallet, amount=5, access=['contact'])
                    contact = applicant.applicant.employeeprofile.phone_number
                    return render(request, 'Accounts/employer/all-applicants.html',
                                  {'contact': contact, 'applicant': all})
            return Http404

