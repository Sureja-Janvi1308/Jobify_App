import re

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from company.models import EmployerProfile, Job, Applicants
from employee.models import Applied_Jobs


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        exclude = ['user']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if re.search(r'[a-zA-Z]', mobile):
            raise forms.ValidationError('Phone number Cannot be consist any letters or alphabets')
        if not re.match('[6-9][0-9]{9}', mobile):
            raise forms.ValidationError('Not a Valid Phone Number')
        return mobile

    def clean_company_name(self):
        company_name = self.cleaned_data['company_name']
        if re.search(r'\d', company_name) or re.search(r'\W', company_name):
            raise forms.ValidationError('Company name should not contain any number or special characters')
        return company_name

    def clean_address_2(self):
        address_1 = self.cleaned_data.get('address_1')
        address_2 = self.cleaned_data.get('address_2')
        if address_1 and address_2 and address_1.lower() == address_2.lower():
            raise forms.ValidationError('Address 1 and Address 2 should not be the same ')
        return address_2


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['user']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicants
        fields = ('job',)


class AppliedJobForm(forms.ModelForm):
    class Meta:
        model = Applied_Jobs
        fields = ('job',)
