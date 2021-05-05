import re

from django.http import HttpRequest, HttpResponse


class MobileVersionMiddleware:
    """
    Middleware for detecting if user agent is mobile
    and set properly flag in request object
    """
    def __init__(self, get_response: HttpRequest) -> None:
        self._get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        mobile_agent_re = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
        if mobile_agent_re.match(request.META['HTTP_USER_AGENT']):
            request.mobile_version = True
        response = self._get_response(request)
        return response


