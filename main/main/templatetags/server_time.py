"""
Custom tag that display current server time
"""
import datetime
from django import template

register = template.Library()

@register.simple_tag
def server_time():
    return datetime.datetime.now().time()