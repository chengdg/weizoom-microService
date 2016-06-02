# -*- coding: utf-8 -*-

import uuid
import json
import logging
from eaglet.core.exceptionutil import unicode_full_stack


class WatchdogClient(object):
    """docstring for WatchdogClient"""
    def __init__(self, service_name):
        super(WatchdogClient, self).__init__()
        self.index = 0
        self.msg = '[watchdog:python]'
        self.service_name = service_name
        self.type = "api"
        self.id = str(uuid.uuid1())

    def getMessge(self, message, user_id, type=None):
        self.index += 1
        if type:
            self.type =  type
        
        try:
            json.dumps(message)
        except:
            message = unicode_full_stack()

        message = {
            "msg": self.msg,
            "service_name": self.service_name,
            "type": self.type,
            "id": self.id,
            "index":  self.index,
            "message": message,
            "userId": user_id
        }
        return json.dumps(message)