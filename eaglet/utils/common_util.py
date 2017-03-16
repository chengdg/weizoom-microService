# -*- coding: utf-8 -*-
import datetime


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