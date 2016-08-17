# -*- coding: utf-8 -*-

try:
	import settings
except:
	from django.conf import settings
import logging

__all__ = []

_DEFAULT_PASSWORD_LENGTH = 32

_DEFAULTS = {
	'DEFAULT_GATEWAY_HOST': 'api.weapp.com',
	# 开启API Auth授权。若不开启，则不加载相应的model
	'ENABLE_API_AUTH': False,
	'API_SCHEME': 'http'
}

for key, value in _DEFAULTS.items():
	try:
		getattr(settings, key)
	except AttributeError:
		setattr(settings, key, value)
	except ImportError as e:
		logging.info("ImportError: {}".format(e))
		pass
