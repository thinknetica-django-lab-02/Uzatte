from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Profile


class ProfileForm(ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('user',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


ProfileFormSet = inlineformset_factory(User, Profile, fields='__all__',
                                       extra=0, min_num=1, can_delete=False)
