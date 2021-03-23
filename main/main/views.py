from django.shortcuts import render


def index(request):
    """
    View that render default template on root url
    :param request:
    :return: request, path to template
    """
    return render(request, 'main/index.html')
