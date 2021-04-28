from typing import Any, Dict, Union

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser, User
from django.core.cache import cache
from django.db.models import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import GoodForm, ProfileFormSet, UserForm
from .models import Good
from .tasks import send_phone_code


def index(request: HttpRequest) -> HttpResponse:
    """
    View that render default template on root url
    :param request:
    :return: request, path to template
    """
    turn_on_block = True
    context = {
        "turn_on_block": turn_on_block,
    }
    return render(request, 'main/index.html', context)


class GoodList(ListView):
    """
    Generic that displays list of goods
    """
    paginate_by = 10
    model = Good

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        qs = qs.filter(is_publish=True)
        # Get filter parameter from url
        # and passes it got  QuerySet.Filter() method
        # with walrus operator
        if query := self.request.GET.get('tag'):
            return qs.filter(tags__name=query)
        else:
            return qs

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('tag') or ""
        # if query result is None - set it to ""
        # in order to not pass None as text value
        # to tag context in HTML Template
        context['tag'] = query
        return context


class GoodDetail(DetailView):
    """
    Generic that displays detailed info
    about a good
    url: /good/<pk>/
    """
    model = Good

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        obj_count_key: str = f"object_{obj.pk}_count"
        obj_count: int = cache.get(obj_count_key, 0)
        obj_count += 1
        cache.set(obj_count_key, obj_count, timeout=60)
        context['obj_count'] = obj_count
        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name: str = 'main/user_edit.html'
    success_url: str = '/accounts/profile/'
    login_url: str = '/accounts/login/'

    def get_object(self, request: HttpRequest) -> Union[AbstractBaseUser,
                                                        AnonymousUser]:
        return request.user

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileFormSet(
            instance=self.get_object(kwargs['request']))
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object(request)
        return self.render_to_response(self.get_context_data(request=request))

    def form_valid_formset(self, form: Any, formset: Any) -> HttpResponse:
        if formset.is_valid():
            formset.save(commit=False)
            formset.save()
        else:
            return HttpResponseRedirect(self.get_success_url())
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object(request)
        form = self.get_form()
        profile_form = ProfileFormSet(self.request.POST,
                                      self.request.FILES, instance=self.object)
        if form.is_valid():
            return self.form_valid_formset(form, profile_form)
        else:
            return self.form_invalid(form)


class GoodCreate(PermissionRequiredMixin, CreateView):
    model = Good
    form_class = GoodForm
    template_name: str = 'main/good_add.html'
    success_url: str = '/goods/'
    permission_required: tuple = ('main.add_good', 'main.view_good')


class GoodEdit(PermissionRequiredMixin, UpdateView):
    model = Good
    form_class = GoodForm
    template_name = 'main/good_edit.html'
    success_url = '/goods/'
    permission_required = ('main.change_good', 'main.view_good')


def phone_number_confirmation(request: HttpRequest) -> HttpResponse:
    """
    Function for confirmation user phone number
    User can do it at amy moment in his profile
    """
    user = request.user
    user_id = user.pk
    phone_number = str(user.profile.phone_number)
    confirmation_flag = user.profile.phone_confirmed
    if not confirmation_flag and phone_number:
        send_phone_code.delay(phone_number, user_id)
        confirm_message = "We sent 4 digit code to your phone"
        request.session['confirm_message'] = confirm_message
        return redirect('profile')
    else:
        confirm_message = 'You have already confirmed you phone number'
        request.session['confirm_message'] = confirm_message
        return redirect('profile')
