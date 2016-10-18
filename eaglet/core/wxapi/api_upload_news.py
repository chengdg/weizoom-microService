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
	https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token=ACCESS_TOKEN
	
	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

	4.格式化post数据

	参数信息：
	参数	         是否必须	   说明
	Articles	      是	 图文消息，一个图文消息支持1到10条图文
	thumb_media_id	  是	 图文消息缩略图的media_id，可以在基础支持-上传多媒体文件接口中获得
	author	          否	 图文消息的作者
	title	          是	 图文消息的标题
	content_source_url	 否	 在图文消息页面点击“阅读原文”后的页面
	content	          是	 图文消息页面的内容，支持HTML标签
	digest	 		  否	 图文消息的描述
		
		{
		   "articles": [
				 {
                    "thumb_media_id":"qI6_Ze_6PtV7svjolgs-rN6stStuHIjs9_DidOHaj0Q-mwvBelOXCFZiq2OsIU-p",
                    "author":"xxx",
					"title":"Happy Day",
					"content_source_url":"www.qq.com",
					"content":"content",
					"digest":"digest"
				 },
				 {
		            "thumb_media_id":"qI6_Ze_6PtV7svjolgs-rN6stStuHIjs9_DidOHaj0Q-mwvBelOXCFZiq2OsIU-p",
		            "author":"xxx",
					"title":"Happy Day",
					"content_source_url":"www.qq.com",
					"content":"content",
					"digest":"digest"
				 }
		   ]
		}
"""

DEFAULT_CONTENT = u'↓↓↓详情请点击'
class Articles(object):
	ARTICLES = 'articles'
	THUMB_MEDIA_ID = 'thumb_media_id'
	TITLE = 'title'
	CONTENT = 'content'
	CONTENT_SOURCE_URL = 'content_source_url'
	AUTHOR = 'author'
	DIGEST = 'digest'
	SHOW_COVER_PIC = 'show_cover_pic'

	def __init__(self):
		self.articles = []

	def add_article(self, thumb_media_id, title, content, content_source_url=None, author=None, digest=None):

		article_dict = {}
		if title == None or title == '':
			raise ValueError(u'图文标题不能为空')
		article_dict[self.TITLE] = title

		if thumb_media_id == None or thumb_media_id == '':
			raise ValueError(u'thumb_media_id不能为空')
		article_dict[self.THUMB_MEDIA_ID] = thumb_media_id

		if content == None or content == '':
			content = DEFAULT_CONTENT
		article_dict[self.CONTENT] = content

		if content_source_url:
			article_dict[self.CONTENT_SOURCE_URL] = content_source_url		

		if author:
			article_dict[self.AUTHOR] = author		

		if digest:
			article_dict[self.DIGEST] = digest

		article_dict[self.SHOW_COVER_PIC] = 0
		self.articles.append(article_dict)

	def get_article_json_str(self):
		return json.dumps({self.ARTICLES: self.articles})
			
SEND_CUSTOM_MSG_URI = 'cgi-bin/media/uploadnews'
class WeixinUploadNewsApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) > 2 and len(varargs) == 0:
			raise ValueError(u'WeixinUploadNewsApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinUploadNewsApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'发送客服消息'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args =（sendto_openid, custom_msg_instance	
	###############################################################################
	def parese_post_param_json_str(self, args):
		
		if isinstance(args[0], Articles) is False:
			raise ValueError(u'WeixinUploadNewsApi param TextCustomMessage illegal')			

		return args[0].get_article_json_str()

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				api_settings.WEIXIN_API_DOMAIN,
				SEND_CUSTOM_MSG_URI,
				param_dict
				)

	def is_retry(self, args):
		if len(args) == 2:
			return True if args[1] is True else False
		return False