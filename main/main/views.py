from django.shortcuts import render
from django.views.generic import ListView
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
    model = Good