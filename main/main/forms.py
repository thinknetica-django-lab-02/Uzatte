from allauth.account.forms import SignupForm

from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

from .models import Good, Profile


class ProfileForm(forms.ModelForm):
    """
    Form for editing user's additional profile
    """
    user = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('birth_date', 'user')


class UserForm(forms.ModelForm):
    """
        Form for editing user's profile
        """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


ProfileFormSet = inlineformset_factory(User, Profile,
                                       fields=('birth_date',
                                               'user',
                                               'phone_number',
                                               'image'),
                                       extra=0, min_num=1, can_delete=False)


class GoodForm(forms.ModelForm):
    """
    Form for adding and editing Goods
    """
    class Meta:
        model = Good
        fields = ('name', 'description', 'price', 'manufacturer',
                  'seller', 'category', 'tags')


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
