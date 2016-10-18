# -*- coding: utf-8 -*-

__author__ = 'paco bert'

import json
from utils.url_helper import complete_get_request_url
import api_settings
from util import *
from custom_message import build_custom_message_json_str, TextCustomMessage

""""
	调用用户信息api:
	http请求方式: POST
	https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token=ACCESS_TOKEN
	
	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

	4.格式化post数据
		(1) 图文
		{
		   "touser":[
		    "OPENID1",
		    "OPENID2"
		   ],
		   "mpnews":{
		      "media_id":"123dsdajkasd231jhksad"
		   },
		    "msgtype":"mpnews"
		}
	   (2) 文本
		{
   		"touser": [
		    "OPENID1",
		    "OPENID2"
		   ],
		   "msgtype": "text", 
		   "text": { "content": "hello from boxer."}
		}
"""
MEDIA_ID = 'media_id'
TOUSER = 'touser'
TYPE = 'msgtype'

class MassMessage(object):
	def __init__(self):
		raise NotImplementedError
	
class NewsMessage(MassMessage):
	MSGTYPE = 'mpnews'
			
	def __init__(self, openid_list, media_id):
		if media_id == None or media_id == '':
			raise ValueError(u'media_id con not be none or ""')
		if len(openid_list) == 0:
			raise ValueError(u'openid list can not be none')

		self.openid_list = openid_list
		self.media_id = media_id

	def get_message_json_str(self):
		return json.dumps({TOUSER : self.openid_list, TYPE : self.MSGTYPE, self.MSGTYPE: {MEDIA_ID: self.media_id}})

class TextMessage(MassMessage):
	MSGTYPE = 'text'
	CONTENT = 'content'

	def __init__(self, openid_list, content):
		if content == None or content == '':
			raise ValueError(u'content con not be none or ""')
		if len(openid_list) == 0:
			raise ValueError(u'openid list can not be none')

		self.openid_list = openid_list
		self.content = content

	def get_message_json_str(self):
		return json.dumps({TOUSER : self.openid_list, TYPE : self.MSGTYPE, self.MSGTYPE: {self.CONTENT : self.content}})


SEND_MASS_MSG_URI = 'cgi-bin/message/mass/send'
class WeixinMassSendApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) >= 3 and len(varargs) == 0:
			raise ValueError(u'WeixinMassSendApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinMassSendApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'发送客服消息'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args =（sendto_openid, custom_msg_instance	
	###############################################################################
	def parese_post_param_json_str(self, args):
		
		if isinstance(args[0], MassMessage) is False:
			raise ValueError(u'WeixinMassSendApi param MassMessage illegal')			

		return args[0].get_message_json_str()

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				api_settings.WEIXIN_API_DOMAIN,
				SEND_MASS_MSG_URI,
				param_dict
				)

	def is_retry(self, args):
		if len(args) == 2:
			return True if args[1] is True else False
		return False