from django import forms
from .models import Profile
from django.core.exceptions import ValidationError

import datetime
from dateutil.relativedelta import relativedelta


class ProfileForm(forms.ModelForm):
    """
    Form for editing user's profile
    """
    first_name = forms.CharField(max_length=120, label="Имя пользователя")
    last_name = forms.CharField(max_length=120, label="Фамилия пользователя")
    email = forms.EmailField(label="email")

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'birth_date')

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        now_date = datetime.datetime.now().date()
        difference_in_years = relativedelta(now_date, birth_date).years
        if difference_in_years < 18:
            raise ValidationError("Age must be more that 18")
        else:
            return birth_date
