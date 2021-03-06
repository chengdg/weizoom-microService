# -*- coding: utf-8 -*-

import json
import logging
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.utils import pson
import datetime


class WatchdogClient(object):
	"""docstring for WatchdogClient"""

	def __init__(self, service_name):
		super(WatchdogClient, self).__init__()
		self.index = 0
		self.msg = '[watchdog:python]'
		self.service_name = service_name
		self.version = "1.0.1"

	def getMessge(self, level, message, log_type, log_id):
		self.index += 1
		if log_type:
			self.log_type = log_type
		self.log_id = log_id
		try:
			err_msg = ''
			json.dumps(message)
		except:
			message = str(message)
			err_msg = unicode_full_stack()

		# message = {
		# 	"msg": self.msg,
		# 	"service_name": self.service_name,
		# 	"type": self.type,
		# 	"uuid": self.id,
		# 	"index": self.index,
		# 	"xmessage": message,  # 兼容elk，字段名不能为message
		# 	"json_error": err_msg
		# }

		message = {
			"msg": self.msg,
			"service_name": self.service_name,
			"type": self.log_type,
			"uuid": self.log_id,
			"index": self.index,
			"xmessage": message,  # 兼容elk，字段名不能为message
			"json_error": err_msg,
			"level": level,
			"datetime": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
			'version': self.version
		}

		# log = json.dumps(message) + ":::" + pson.dumps(message)

		# log = json.dumps({
		# 	'json_log': message,
		# 	# 'pson_log': pson.dumps(message, stringify=False)
		# 	'pson_log': pson.dumps(message)
		# })
		log = pson.dumps(message)
		return log
