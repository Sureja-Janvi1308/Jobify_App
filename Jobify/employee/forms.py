import re

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, ButtonHolder
from crispy_forms.bootstrap import FormActions
from django import forms

from .models import EmployeeProfile, Education, Experience, Skill


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        exclude = ['user']
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address_1', 'address_2', 'city', 'state',
                  'pincode', 'country', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if re.search(r'[a-zA-Z]', phone_number):
            raise forms.ValidationError('Phone number Cannot be consist any letters or alphabets')
        if not re.match('[6-9][0-9]{9}', phone_number):
            raise forms.ValidationError('Not a Valid Phone Number')
        return phone_number

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.is_alpha():
            raise forms.ValidationError('First name should consist of only letters')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.is_alpha():
            raise forms.ValidationError('Last name should consist of only letters')
        return last_name

    def clean_address_2(self):
        address_1 = self.cleaned_data.get('address_1')
        address_2 = self.cleaned_data['address_2']
        if address_2 and address_1 and address_1.lower() and address_2.lower():
            raise forms.ValidationError('Address1 and Address2 should not be the same')
        return address_2



    def set_initial_user_data(self, user):
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['user', 'user_id']
        fields = ['institution_name', 'degree', 'field_of_study', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = self._set_form_helper()

    def _set_form_helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.layout = Layout(
            Field('institution_name', css_class='form-control'),
            Field('degree', css_class='form-control'),
            Field('field_of_study', css_class='form-control'),
            Field('start_date', css_class='form-control'),
            Field('end_date', css_class='form-control'),

        )
        helper.layout.append(ButtonHolder(Submit('submit', 'Submit', css_class='btn btn-primary')))
        return helper


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['user']
        fields = ['company_name', 'job_title', 'start_date', 'end_date', 'description']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Save'))


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = [' user']
        fields = ['name', 'years_of_experience']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Save'))
