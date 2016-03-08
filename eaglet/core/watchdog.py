# -*- coding: utf-8 -*-

"""@package eaglet.core.watchdog

Watchdog接口
"""
__author__ = 'duhao'
import logging

DEBUG = 1
INFO = 2
WARNING = 3
ERROR = 4
ALERT = 5
logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s %(message)s', 
        datefmt="%Y-%m-%d %H:%M:%S", 
        level=logging.INFO
    )

def debug(service_name, message, log_type='WEB', user_id='0'):
	__watchdog(service_name, message, DEBUG, log_type, user_id)


def info(service_name, message, log_type='WEB', user_id='0'):
	__watchdog(service_name, message, INFO, log_type, user_id)


def warning(service_name, message, log_type='WEB', user_id='0'):
	__watchdog(service_name, message, WARNING, log_type, user_id)


def error(service_name, message, log_type='WEB', user_id='0'):
	__watchdog(service_name, message, ERROR, log_type, user_id)


def alert(service_name, message, log_type='WEB', user_id='0'):
	__watchdog(service_name, message, ALERT, log_type, user_id)


def __watchdog(service_name, message, level, log_type, user_id):
	"""
	@param[in] level 日志级别
	@param[in] message 日志信息，通常是json格式
	@param[in] log_type 日志类型，如WEB, API, H5
	@param[in] user_id 系统账号的user id，用来追踪是哪个用户的系统中出的问题
	"""
	if type(user_id) == int:
		user_id = str(user_id)

	#由于logging的限制，自定义的输出信息都拼装到message里进行打印
	message = '%s %s %s %s' % (service_name, log_type, user_id, message)
	if level == DEBUG:
		logging.debug(message)
	elif level == INFO:
		logging.info(message)
	elif level == WARNING:
		logging.warn(message)
	elif level == ERROR:
		logging.error(message)
	elif level == ALERT:
		logging.critical(message)