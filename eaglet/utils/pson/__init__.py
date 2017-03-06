# -*- coding: UTF-8 -*-
import datetime
import json

import six
from decimal import Decimal


def is_base_type(obj):
	"""Determine if the object instance is of a protected type.

	Objects of protected types are preserved as-is when passed to
	force_text(strings_only=True).
	"""
	return isinstance(obj,
	                  six.integer_types + (
		                  type(None), float, basestring, Decimal, datetime.datetime, datetime.date, datetime.time))


def convert2string(obj, stringify):
	if stringify:
		return json.dumps(obj)
	else:
		return obj

def get_path_value(data, stringify):
	def _get_format_str(path, v):
		return "{}={}".format(path, convert2string(v, stringify))

	def _recursive_get(data, res, path='/'):

		delim = '/' if path != '/' else ''

		if isinstance(data, dict):
			for k, v in data.iteritems():
				new_path = delim.join([path, k])

				if is_base_type(v):
					res.append(_get_format_str(new_path, v))
				else:
					_recursive_get(v, res, new_path)
		elif isinstance(data, list):
			for i, v in enumerate(data):

				if is_base_type(v):
					res.append(_get_format_str(path, v))
				else:
					_recursive_get(v, res, delim.join([path, str(i)]))
		else:
			res.append("ERROR")

	result = []
	_recursive_get(data, result)

	return result


def dumps(data, stringify=True):

	result = get_path_value(data, stringify=stringify)

	# return ("{" + ",".join(result) + "}").replace('"', '')
	return ("{" + ",".join(result) + "}")