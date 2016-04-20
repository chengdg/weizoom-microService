# -*- coding: utf-8 -*-

import settings
from core.zipkin import zipkin_client

class ZipkinMiddleware(object):
	"""docstring for ZipkinMiddleware"""
	def process_request(self, request, response):

		zid = request.params.get('zid', None)
		zdepth = request.params.get('zdepth', 1)
		if zid:
			zipkin_client.zipkinClient = zipkin_client.ZipkinClient(zid, zdepth)
			#request.params['zipkin_client'] = zipkin_client.zipkinClient 
		