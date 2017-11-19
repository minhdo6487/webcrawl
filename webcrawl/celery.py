from __future__ import absolute_import

import os

from celery import Celery
import celery.bin.celery
import celery.bin.base
import celery.platforms
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcrawl.settings')

from django.conf import settings  # noqa

app = Celery('webcrawl', broker='redis://localhost:6379/0')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# status = celery.bin.celery.CeleryCommand.commands['status']()
# status.app = status.get_app()
#
# @app.task(bind=True)
# def debug_task(self):
#     from celery_app.tasks import increase
#     increase.count(3)
#     # print('Request: {0!r}'.format(self.request))
#     pass


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# @app.task
# def push_notification_tick():
# 	from core.tasks import push_notification_send_campaign
# 	push_notification_send_campaign()

@app.task
def task_number_one():
    print ("minh")
    return "minh"