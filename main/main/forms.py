from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

from .models import Good, Profile



class ProfileForm(forms.ModelForm):
    """
    Form for editing user's profile
    """
    user = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('birth_date', 'user')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


ProfileFormSet = inlineformset_factory(User, Profile, fields='__all__',
                                       extra=0, min_num=1, can_delete=False)



class GoodForm(forms.ModelForm):
    """
    Form for adding and editing Goods
    """
    class Meta:
        model = Good
        fields = ('name', 'description', 'price', 'manufacturer',
                  'seller', 'category', 'tags')

