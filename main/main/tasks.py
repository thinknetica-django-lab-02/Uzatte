from celery.schedules import crontab
from .mails import week_news_notifications
from .celery import app as celery_app


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(second=30), week_news_notifications.s())
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')


@celery_app.task
def test(arg):
    print(arg)