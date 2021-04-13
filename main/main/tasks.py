import datetime

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import main.models as models

from .celery import app as celery_app


@celery_app.task
def week_news_notifications():
    now = datetime.datetime.now()
    week = datetime.timedelta(days=7)
    d = now - week
    goods = models.Good.objects.filter(publish_date__gte=d)
    email_set = {subscriber.user.email for subscriber
                 in models.Subscriber.objects.all()}
    subject = 'Новый товар!'
    context = {
        "goods": goods,
    }
    html_message = render_to_string('account/week_mail.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'From <one@ecommerce.com>'
    mail.send_mail(subject, plain_message, from_email, email_set,
                   html_message=html_message)


# Send mail for every new good
@celery_app.task
def send_mail_notification(subject, plain_message, from_email, email_set,
                           html_message):
    mail.send_mail(subject, plain_message, from_email, email_set,
                   html_message=html_message)
