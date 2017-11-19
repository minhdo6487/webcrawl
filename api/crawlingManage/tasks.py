from __future__ import absolute_import, unicode_literals
from celery import task, Task
from lib import infomation_extract
from celery.app.registry import TaskRegistry

from lib.infomation_extract import extract_feed, extract_data
#
@task()
def task_number_one():
    print ("minh")
    return "minh"

@task()
def crawl_feed():
    url = "https://nhattao.com/"
    ef = extract_feed(url)
    data = ef.get_feed()

@task()
def crawl_data():
    url = "https://nhattao.com/"
    ea = extract_data(url)
    tmp = ea.get_all_sub_link
    ea.get_info(tmp)