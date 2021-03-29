from django.shortcuts import render
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.models import User
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
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
    login_url = "/admin/login/?next=/accounts/profile/"
    model = User
    form_class = ProfileForm
    template_name = 'main/user_edit.html'
    success_url = '/accounts/profile/'

    def get_object(self, queryset=None):
        return self.request.user
