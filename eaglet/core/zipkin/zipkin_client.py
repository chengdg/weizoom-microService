# -*- coding: utf-8 -*-

import json
import logging
import settings

TYPE_CALL_SERVICE = 3
TYPE_CALL_REDIS = 1
TYPE_CALL_MYSQL = 2

class ZipkinClient(object):
	"""docstring for ZipkinClient"""
	def __init__(self, zid, zdepth):
		super(ZipkinClient, self).__init__()
		self.zid = zid
		self.zdepth = int(zdepth) + 1
		self.zindex = 1
		self.msg = '[zipkin:python]'
		self.service = settings.SERVICE_NAME
		print ">>>>>>>>>>>"

	def sendMessge(self, type, responseTime, method='', resource='', data='', isCallDownstream=0):
		self.zindex += 1
		self.type = type
		self.responseTime = responseTime
		self.method = method
		self.resource = resource
		self.data = data
		self.isCallDownstream = isCallDownstream

		data =  self.getData()
		logging.info(json.dumps(data))


	def getData(self):
		return {
			"msg": self.msg,
			"service": self.service,
			"type": self.type,
			"zid": self.zid,
			"zdepth":  self.zdepth,
			"zindex": self.zindex,
			"isCallDownstream": self.isCallDownstream,
			"responseTime": self.responseTime,
			"resource": self.resource,
			"method": self.method,
			"data": self.data,
		}

