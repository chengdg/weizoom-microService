# -*- coding: utf-8 -*-
"""
@package eaglet.utils.resouce_client
访问API的client

"""

import json
import urllib
import urlparse
import uuid

import requests
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core.zipkin import zipkin_client
#from eaglet.core.zipkin.zipkin_client import ZipkinClient
from time import time
import logging

try:
	import settings
except:
	from django.conf import settings



# def conn_try_again(function):
# 	RETRIES = 0
# 	# 重试的次数
# 	count = {"num": RETRIES}
#
# 	def wrapped(*args, **kwargs):
# 		try:
# 			return function(*args, **kwargs)
# 		except Exception as e:
# 			if count['num'] < DEFAULT_RETRY_COUNT:
# 				count['num'] += 1
# 				return wrapped(*args, **kwargs)
# 			else:
# 				return False, None
#
# 	return wrapped


def url_add_params(url, **params):
	""" 在网址中加入新参数 """
	pr = urlparse.urlparse(url)
	query = dict(urlparse.parse_qsl(pr.query))
	query.update(params)
	prlist = list(pr)
	prlist[4] = urllib.urlencode(query)
	return urlparse.ParseResult(*prlist).geturl()


class Inner(object):

	def __get_auth(self):
		# 获取access_token
		res = self.get({
			'resource': 'auth.access_token',
			'data': {
				'app_key': settings.APP_KEY,
				'app_secret': settings.APP_SECRET,
				#'woid': 0
				}
			})
		# TODO: 需缓存access_token
		access_token = None
		if res and res['code']==200:
			# 表示业务成功
			data = res['data']
			access_token = data['access_token']
			# data['expire_time']
			logging.info("Got access_token from API service")
		else:
			logging.info("Failed to get `access_token`, resp: {}".format(res))
		#self.access_token = access_token
		return access_token


	def __init__(self, service, gateway_host):
		self.access_token = None
		self.service = service
		self.gateway_host = gateway_host
		if gateway_host.find('://')<0:
			# 如果没有scheme，则自动补全
			self.gateway_host = "%s://%s" % (settings.DEFAULT_API_SCHEME, gateway_host)
		logging.info(u"gateway_host: {}".format(self.gateway_host))

		self.__resp = None
		self.access_token = self.__get_auth() if settings.ENABLE_API_AUTH else None

	def get(self, options):
		return self.__request(options['resource'], options['data'], 'get')

	def put(self, options):
		return self.__request(options['resource'], options['data'], 'put')

	def post(self, options):
		return self.__request(options['resource'], options['data'], 'post')

	def delete(self, options):
		return self.__request(options['resource'], options['data'], 'delete')

	def __request(self, resource, params, method):
		# 构造url
		"""

		@return is_success,code,data
		"""

		host = self.gateway_host

		resource_path = resource.replace('.', '/')

		if self.service:
			base_url = '%s/%s/%s/' % (host, self.service, resource_path)
		else:
			# 如果resouce为None，则URL中省略resource。方便本地调试。
			base_url = '%s/%s/' % (host, resource_path)

		# zipkin支持
		if hasattr(zipkin_client, 'zipkinClient') and zipkin_client.zipkinClient:
			zid = zipkin_client.zipkinClient.zid
			zindex = zipkin_client.zipkinClient.zindex
			fZindex = zipkin_client.zipkinClient.fZindex
			zdepth = zipkin_client.zipkinClient.zdepth
			zipkinClient = zipkin_client.zipkinClient
		else:
			zid = str(uuid.uuid1())
			zindex = 1
			fZindex = 1
			zdepth = 1
			zipkinClient = zipkin_client.ZipkinClient(self.service, zid, zdepth, fZindex)
			

		url = url_add_params(base_url, zid=zid, zindex=zindex, f_zindex=str(fZindex) + '_' + str(zindex),
		                     zdepth=zdepth + 1)

		start = time()
		try:
			# 访问资源
			if self.access_token:
				params['access_token'] = self.access_token

			if method == 'get':
				resp = requests.get(url, params=params, timeout=settings.DEFAULT_TIMEOUT)
			elif method == 'post':
				resp = requests.post(url, data=params, timeout=settings.DEFAULT_TIMEOUT)
			else:
				# 对于put、delete方法，变更为post方法，且querystring增加_method=put或_method=delete
				url = url_add_params(url, _method=method)
				resp = requests.post(url, data=params, timeout=settings.DEFAULT_TIMEOUT)

			self.__resp = resp

			# 解析响应
			if resp.status_code == 200:

				json_data = json.loads(resp.text)
				code = json_data['code']

				if code == 200 or code == 500:
					self.__log(True, url, params, method)
					return json_data

				else:
					self.__log(False, url, params, method, 'ServiceProcessFailure', 'BUSINESS_CODE:' + str(code))
					return None
			else:
				self.__log(False, url, params, method, 'ServerResponseFailure',
				           'HTTP_STATUS_CODE:' + str(resp.status_code))
				return None

		except requests.exceptions.RequestException as e:
			self.__log(False, url, params, method, str(type(e)), unicode_full_stack())
			return None
		except BaseException as e:
			self.__log(False, url, params, method, str(type(e)), unicode_full_stack())
			return None
		finally:
			stop = time()
			duration = stop - start
			zipkinClient.sendMessge(zipkin_client.TYPE_CALL_SERVICE, duration, method=method, resource='', data='')

	def __log(self, is_success, url, params, method, failure_type='', failure_msg=''):
		msg = {
			'is_success': is_success,
			'url': url,
			'params': params,
			'method': method,
			'failure_type': failure_type,
			'failure_msg': failure_msg,

		}

		resp = self.__resp

		if resp:
			msg['http_code'] = resp.status_code
			msg['resp_text'] = resp.text
		else:
			msg['http_code'] = ''
			msg['resp_text'] = ''

		if is_success:
			watchdog.info(msg, settings.CALL_SERVICE_WATCHDOG_TYPE, server_name=self.service)
		else:
			watchdog.alert(msg, settings.CALL_SERVICE_WATCHDOG_TYPE, server_name=self.service)


class Resource(object):
	@staticmethod
	def use(service, gateway_host=settings.DEFAULT_GATEWAY_HOST):
		return Inner(service, gateway_host)
