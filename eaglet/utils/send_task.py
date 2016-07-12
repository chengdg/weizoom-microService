#coding: utf8
"""@package service.utils.send_task
命令行方式启动Celery task

**用法**：

    from eaglet.core.utils.send_task import send_task

    send_task(queue_name, args)

**说明**：

    <service_name> : 服务(队列名称)的名称。如果在@task中指定name，则为次名字；否则为函数的全名。

**用法举例**：
    
    integarl_log = {
        "member_id":1,
        "nick_name":"weizoom",
        "event_type": "好友通过分享链接购买商品",
        "increase_integral": 100,
        "current_integral": 200
    }
    send_task("services.template_message_integral_service.tasks.service_tempate_message_integral", integarl_log)

"""

from celery import Celery
celery = Celery()
celery.config_from_object('eaglet.core.service.celeryconfig')

from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack



def send_task(queue_name, args):
    try:
        result = celery.send_task(queue_name, args=[args], queue=queue_name)
    except:
        notify_message = u"queue_name:{}, args:{}, cause:\n{}".format(queue_name, args, unicode_full_stack())
        watchdog.error(notify_message)
    
