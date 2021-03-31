from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

from .models import Profile


ProfileInlineFormSet = inlineformset_factory(User, Profile, can_delete=False,
                                             fields=('first_name',
                                                     'last_name', 'email'))
