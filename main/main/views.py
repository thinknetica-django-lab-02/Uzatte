from django.shortcuts import render


def index(request):
    """
    View that render default template on root url
    :param request:
    :return: request, path to template
    """
    turn_on_block = False
    context = {
        "turn_on_block": turn_on_block,
        "username": "Admin",
    }
    return render(request, 'main/index.html', context)
