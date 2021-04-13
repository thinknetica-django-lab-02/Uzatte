import datetime

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .celery import app as celery_app
from .models import Good, Subscriber


@celery_app.task
def week_news_notifications():
    now = datetime.datetime.now()
    week = datetime.timedelta(days=7)
    d = now - week
    goods = Good.objects.filter(publish_date__gte=d)
    email_set = {subscriber.user.email for subscriber
                 in Subscriber.objects.all()}
    subject = 'Новый товар!'
    context = {
        "goods": goods,
    }
    html_message = render_to_string('account/week_mail.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'From <one@ecommerce.com>'
    mail.send_mail(subject, plain_message, from_email, email_set,
                   html_message=html_message)
