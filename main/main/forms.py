from django import forms
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    """
    Form for editing user's profile
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
