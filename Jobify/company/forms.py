import re

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from company.models import EmployerProfile, Job, Applicants


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

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if re.search(r'\d', first_name) or re.search(r'\W', first_name):
            raise forms.ValidationError('First name should not contain any number or special characters')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if re.search(r'\d', last_name) or re.search(r'\W', last_name):
            raise forms.ValidationError('Last name should not contain any number or special characters')
        return last_name

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

    def clean_website(self):
        website = self.cleaned_data['website']
        if not re.search(r'^https?://\w+\./w+$', website):
            raise forms.ValidationError('Invalid Website URL')
        return website

    def set_initial_user_data(self, user):
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email


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

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.is_alnum():
            raise forms.ValidationError('title should not contain any special characters')
        return title

    def clean_salary(self):
        salary = self.cleaned_data['salary']
        if not salary.is_numeric():
            raise forms.ValidationError('salary should be written in numbers only')
        return salary

    def clean_position(self):
        position = self.cleaned_data['position']
        if not position.is_numeric():
            raise forms.ValidationError('No of position required should be in numbers only')
        return position


class ApplyJobForm(forms.ModelForm):

    class Meta:
        model = Applicants
        fields = ('job',)
