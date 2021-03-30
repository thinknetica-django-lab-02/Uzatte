from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form for editing user's profile
    """
    model = Profile
    first_name = forms.CharField(max_length=120, label="Имя")
    last_name = forms.CharField(max_length=120, label="Фамилия")
    email = forms.CharField(label="email")

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']
