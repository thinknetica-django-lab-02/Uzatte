from django import forms
from .models import Profile
from django.core.exceptions import ValidationError

import datetime
from dateutil.relativedelta import relativedelta


class ProfileForm(forms.ModelForm):
    """
    Form for editing user's profile
    """
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'birth_date')

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        now_date = datetime.datetime.now().date()
        difference_in_years = relativedelta(birth_date, now_date).years
        if difference_in_years < 18:
            raise ValidationError("Age must be more that 18")
