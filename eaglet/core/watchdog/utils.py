# -*- coding: utf-8 -*-

#coding:utf8
"""@package weapp.watchdog.utils

Watchdog接口
需要settings里面配置SERVICE_NAME和设置logging格式
logging.basicConfig(
	format='%(servicename)s %(type)s %(process)s %(asctime)s %(levelname)s %(message)s', 
	datefmt="%Y-%m-%d %H:%M:%S", 
	level=logging.INFO
)
"""

import settings

__author__ = 'duhao'
SERVICE_NAME = settings.SERVICE_NAME

def watchdog_debug(message, type='WEB', user_id='0'):
	"""
	用异步方式发watchdog

	异步方式调用 weapp.services.send_watchdog_service.send_watchdog()
	"""
	result = None
	if not celeryconfig.CELERY_ALWAYS_EAGER:
		if WATCHDOG_DEBUG >= settings.WATCH_DOG_LEVEL:
			result = send_watchdog.delay(type, message, WATCHDOG_DEBUG, user_id, db_name)
	else:
		if WATCHDOG_DEBUG >= settings.WATCH_DOG_LEVEL:
			_watchdog(type, message, WATCHDOG_DEBUG, user_id, db_name)
	return result
	#print message


def watchdog_info(message, type='WEB', user_id='0'):
	"""
	用异步方式发watchdog

	异步方式调用 weapp.services.send_watchdog_service.send_watchdog()
	"""
	result = None
	if not celeryconfig.CELERY_ALWAYS_EAGER:
		if WATCHDOG_INFO >= settings.WATCH_DOG_LEVEL:
			result = send_watchdog.delay(type, message, WATCHDOG_INFO, user_id, db_name)
	else:
		if WATCHDOG_INFO >= settings.WATCH_DOG_LEVEL:
			_watchdog(type, message, WATCHDOG_INFO, user_id, db_name)	
	return result

def watchdog_warning(message, type='WEB', user_id='0'):
	"""
	用异步方式发watchdog

	异步方式调用 weapp.services.send_watchdog_service.send_watchdog()
	"""
	result = None
	if not celeryconfig.CELERY_ALWAYS_EAGER:
		if WATCHDOG_WARNING>= settings.WATCH_DOG_LEVEL:
			result = send_watchdog.delay(type, message, WATCHDOG_WARNING, user_id, db_name)
	else:
		if WATCHDOG_NOTICE >= settings.WATCH_DOG_LEVEL:
			_watchdog(type, message, WATCHDOG_NOTICE, user_id, db_name)
	return result


def watchdog_error(message, type='WEB', user_id='0'):
	result = None
	if not celeryconfig.CELERY_ALWAYS_EAGER:
		if WATCHDOG_ERROR >= settings.WATCH_DOG_LEVEL:
			result = send_watchdog.delay(type, message, WATCHDOG_ERROR, user_id, db_name)
		if settings.DEBUG and (not noraise):
			exception_type, value, tb = sys.exc_info()
			if exception_type:
				raise exception_type, exception_type(value), sys.exc_info()[2]
	else:
		if WATCHDOG_ERROR >= settings.WATCH_DOG_LEVEL:
			_watchdog(type, message, WATCHDOG_ERROR, user_id, db_name)
		if settings.DEBUG and (not noraise):
			exception_type, value, tb = sys.exc_info()
			if exception_type:
				raise exception_type, exception_type(value), sys.exc_info()[2]
	return result


def watchdog_alert(message, type='WEB', user_id='0'):
	result = None
	if not celeryconfig.CELERY_ALWAYS_EAGER:
		if WATCHDOG_ALERT >= settings.WATCH_DOG_LEVEL:
			send_watchdog.delay(type, message, WATCHDOG_ALERT, user_id, db_name)
	else:
		if WATCHDOG_ALERT >= settings.WATCH_DOG_LEVEL:
			_watchdog(type, message, WATCHDOG_ALERT, user_id, db_name)
	return result


def __watchdog(message, type, user_id='0'):

	logging.debug(message)