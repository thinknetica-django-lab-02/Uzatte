from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form for editing user's profile
    """
    model = Profile

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']
