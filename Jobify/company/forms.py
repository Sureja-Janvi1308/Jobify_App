import re

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from company.models import EmployerProfile


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
