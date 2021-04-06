from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import GoodForm, ProfileFormSet, UserForm
from .models import Good


def index(request):
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

    def get_queryset(self):
        qs = super().get_queryset()
        # Get filter parameter from url
        # and passes it got  QuerySet.Filter() method
        # with walrus operator
        if query := self.request.GET.get('tag'):
            return qs.filter(tags__name=query)
        else:
            return qs

    def get_context_data(self, **kwargs):
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


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'main/user_edit.html'
    success_url = '/accounts/profile/'
    login_url = '/accounts/login/'

    def get_object(self, request):
        return request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileFormSet(
            instance=self.get_object(kwargs['request']))
        return context

    def get(self, request, *args, **kwargs):

        self.object = self.get_object(request)
        return self.render_to_response(self.get_context_data(request=request))

    def form_valid_formset(self, form, formset):
        if formset.is_valid():
            formset.save(commit=False)
            formset.save()
        else:
            return HttpResponseRedirect(self.get_success_url())
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(request)
        form = self.get_form()
        profile_form = ProfileFormSet(self.request.POST,
                                      self.request.FILES, instance=self.object)
        if form.is_valid():
            return self.form_valid_formset(form, profile_form)
        else:
            return self.form_invalid(form)


class GoodCreate(LoginRequiredMixin, CreateView):
    login_url = "/admin/login/?next=/accounts/profile/"
    model = Good
    form_class = GoodForm
    template_name = 'main/good_add.html'
    success_url = '/goods/'


class GoodEdit(LoginRequiredMixin, UpdateView):
    login_url = "/admin/login/?next=/accounts/profile/"
    model = Good
    form_class = GoodForm
    template_name = 'main/good_edit.html'
    success_url = '/goods/'
