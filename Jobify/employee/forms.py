import re

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, ButtonHolder
from crispy_forms.bootstrap import FormActions
from django import forms

from .models import EmployeeProfile, Education, Experience, Skill


class EmployeeProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeProfileForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['email'].label = "Email Address"
        self.fields['phone_number'].label = "Phone Number"
        self.fields['address_1'].label = "Address Line 1"
        self.fields['address_2'].label = "Address Line 2"
        self.fields['city'].label = "Enter city"
        self.fields['state'].label = "Enter State"
        self.fields['pincode'].label = "Enter pincode"
        self.fields['country'].label = " Choose Country"
        self.fields['profile_pic'].label = "Profile Picture"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone Number',
            }
        )
        self.fields['address_1'].widget.attrs.update(
            {
                'placeholder': 'Enter Address line 1',
            }
        )
        self.fields['address_2'].widget.attrs.update(
            {
                'placeholder': 'Enter Address line 2',
            }
        )
        self.fields['city'].widget.attrs.update(
            {
                'placeholder': 'Enter City',
            }
        )
        self.fields['state'].widget.attrs.update(
            {
                'placeholder': 'Enter State',
            }
        )
        self.fields['pincode'].widget.attrs.update(
            {
                'placeholder': 'Enter Pincode',
            }
        )
        self.fields['country'].widget.attrs.update(
            {
                'placeholder': 'Choose Country',
            }
        )
        self.fields['profile_pic'].widget.attrs.update(
            {
                'placeholder': 'Upload Your Profile Picture',
            }
        )

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
        fields = ['company_name', 'job_title','start_date', 'end_date', 'description']

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





