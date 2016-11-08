# -*- coding: utf-8 -*-
import os

import re

import six
from decimal import Decimal
import datetime

import sys


def get_uncaught_exception_data(req, exc_type, exc_value, tb):
	"""
	返回值结构：
	- sys_path: sys.path
	- server_time: 系统时间
	- sys_version_info： python版本
	- sys_executable：sys.executable
	- exception_type：异常类型
	- exception_value： 异常值
	- req_params:请求参数
	- frames：堆栈列表
		- filename：文件路径
		- pre_context：前面的行
		- context_line: 异常发生的行
		- post_context：后面的行
		- vars：变量
			- key
			- value
	@param req:
	@param exc_type:
	@param exc_value:
	@param tb:
	@return:
	"""
	reporter = ExceptionReporter(req, exc_type, exc_value, tb)
	data = reporter.get_traceback_data()
	return data


def is_protected_type(obj):
	"""Determine if the object instance is of a protected type.

	Objects of protected types are preserved as-is when passed to
	force_text(strings_only=True).
	"""
	return isinstance(obj, six.integer_types + (type(None), float, Decimal,
	                                            datetime.datetime, datetime.date, datetime.time))


def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
	"""
	Similar to smart_text, except that lazy instances are resolved to
	strings, rather than kept as lazy objects.

	If strings_only is True, don't convert (some) non-string-like objects.
	"""
	# Handle the common case first, saves 30-40% when s is an instance of
	# six.text_type. This function gets called often in that setting.
	if isinstance(s, six.text_type):
		return s
	if strings_only and is_protected_type(s):
		return s
	try:
		if not isinstance(s, six.string_types):
			if hasattr(s, '__unicode__'):
				try:
					s = s.__unicode__()
				except:

					s = 'force_text with  __unicode__() error'
			else:
				if six.PY3:
					if isinstance(s, bytes):
						s = six.text_type(s, encoding, errors)
					else:
						s = six.text_type(s)
				else:
					s = six.text_type(bytes(s), encoding, errors)
		else:
			# Note: We use .decode() here, instead of six.text_type(s, encoding,
			# errors), so that if s is a SafeBytes, it ends up being a
			# SafeText at the end.
			s = s.decode(encoding, errors)
	except UnicodeDecodeError as e:

		# If we get to here, the caller has passed in an Exception
		# subclass populated with non-ASCII bytestring data without a
		# working unicode method. Try to handle this without raising a
		# further exception by individually forcing the exception args
		# to unicode.
		s = 'force_text with UnicodeDecodeError'
	return s


class Promise(object):
	"""
	This is just a base class for the proxy class created in
	the closure of the lazy function. It can be used to recognize
	promises in code.
	"""
	pass


def smart_text(s, encoding='utf-8', strings_only=False, errors='strict'):
	"""
	Returns a text object representing 's' -- unicode on Python 2 and str on
	Python 3. Treats bytestrings using the 'encoding' codec.

	If strings_only is True, don't convert (some) non-string-like objects.
	"""
	if isinstance(s, Promise):
		# The input is the result of a gettext_lazy() call.
		return s
	return force_text(s, encoding, strings_only, errors)


def get_safe_settings():
	return ''


# def force_escape(value):
# 	"""
# 	Escapes a string's HTML. This returns a new string containing the escaped
# 	characters (as opposed to "escape", which marks the content for later
# 	possible escaping).
# 	"""
# 	return value


# def pprint(value):
# 	"""A wrapper around pprint.pprint -- for debugging, really."""
# 	try:
# 		return pformat(value)
# 		# return value
# 	except Exception as e:
# 		return "Error in formatting: %s" % force_text(e, errors="replace")




class ExceptionReporter(object):
	"""
	A class to organize and coordinate reporting on exceptions.
	"""

	def __init__(self, request, exc_type, exc_value, tb):
		self.request = request
		self.exc_type = exc_type
		self.exc_value = exc_value
		self.tb = tb

		self.loader_debug_info = None

		# Handle deprecated string exceptions
		if isinstance(self.exc_type, six.string_types):
			self.exc_value = Exception('Deprecated String Exception: %r' % self.exc_type)
			self.exc_type = type(self.exc_value)

	def format_path_status(self, path):
		if not os.path.exists(path):
			return "File does not exist"
		if not os.path.isfile(path):
			return "Not a file"
		if not os.access(path, os.R_OK):
			return "File is not readable"
		return "File exists"

	def get_traceback_data(self):
		"Return a Context instance containing traceback information."

		frames = self.get_traceback_frames()
		for i, frame in enumerate(frames):
			if 'vars' in frame:
				# from django.template.defaultfilters import force_escape
				frame['vars'] = [{'key': k, 'value': force_text(v)} for k, v in frame['vars']]
			frames[i] = frame

		# unicode_hint = ''
		# if self.exc_type and issubclass(self.exc_type, UnicodeError):
		# 	start = getattr(self.exc_value, 'start', None)
		# 	end = getattr(self.exc_value, 'end', None)
		# 	if start is not None and end is not None:
		# 		unicode_str = self.exc_value.args[1]
		# 		unicode_hint = smart_text(unicode_str[max(start - 5, 0):min(end + 5, len(unicode_str))], 'ascii',
		# 		                          errors='replace')

		c = {

			# 'unicode_hint': unicode_hint,
			'frames': frames,
			'req_params': self.request.params,

			# 'settings': get_safe_settings(),
			'sys_executable': sys.executable,
			'sys_version_info': '%d.%d.%d' % sys.version_info[0:3],
			'server_time': str(datetime.datetime.now()),
			'sys_path': sys.path,

		}
		# Check whether exception info is available
		if self.exc_type:
			c['exception_type'] = self.exc_type.__name__
		if self.exc_value:
			c['exception_value'] = smart_text(self.exc_value, errors='replace')
		# if frames:
		# 	c['lastframe'] = frames[-1]
		return c

	def _get_lines_from_file(self, filename, lineno, context_lines, loader=None, module_name=None):
		"""
		Returns context_lines before and after lineno from file.
		Returns (pre_context_lineno, pre_context, context_line, post_context).
		"""
		source = None
		if loader is not None and hasattr(loader, "get_source"):
			try:
				source = loader.get_source(module_name)
			except ImportError:
				pass
			if source is not None:
				source = source.splitlines()
		if source is None:
			try:
				with open(filename, 'rb') as fp:
					source = fp.read().splitlines()
			except (OSError, IOError):
				pass
		if source is None:
			return None, [], None, []

		# If we just read the source from a file, or if the loader did not
		# apply tokenize.detect_encoding to decode the source into a Unicode
		# string, then we should do that ourselves.
		if isinstance(source[0], six.binary_type):
			encoding = 'ascii'
			for line in source[:2]:
				# File coding may be specified. Match pattern from PEP-263
				# (http://www.python.org/dev/peps/pep-0263/)
				match = re.search(br'coding[:=]\s*([-\w.]+)', line)
				if match:
					encoding = match.group(1).decode('ascii')
					break
			source = [six.text_type(sline, encoding, 'replace') for sline in source]

		lower_bound = max(0, lineno - context_lines)
		upper_bound = lineno + context_lines

		pre_context = source[lower_bound:lineno]
		context_line = source[lineno]
		post_context = source[lineno + 1:upper_bound]

		return lower_bound, pre_context, context_line, post_context

	def get_traceback_frames(self):
		frames = []
		tb = self.tb
		while tb is not None:
			# Support for __traceback_hide__ which is used by a few libraries
			# to hide internal frames.
			if tb.tb_frame.f_locals.get('__traceback_hide__'):
				tb = tb.tb_next
				continue
			filename = tb.tb_frame.f_code.co_filename
			function = tb.tb_frame.f_code.co_name
			lineno = tb.tb_lineno - 1
			loader = tb.tb_frame.f_globals.get('__loader__')
			module_name = tb.tb_frame.f_globals.get('__name__') or ''
			pre_context_lineno, pre_context, context_line, post_context = self._get_lines_from_file(filename, lineno, 7,
			                                                                                        loader, module_name)
			if pre_context_lineno is not None:
				frames.append({
					# 'tb': tb,
					'filename': filename,
					'function': function,
					'vars': self.get_traceback_frame_variables(tb.tb_frame),
					'pre_context': pre_context,
					'context_line': context_line,
					'post_context': post_context,
				})
			tb = tb.tb_next

		return frames

	# def format_exception(self):
	# 	"""
	# 	Return the same data as from traceback.format_exception.
	# 	"""
	# 	import traceback
	# 	frames = self.get_traceback_frames()
	# 	tb = [(f['filename'], f['lineno'], f['function'], f['context_line']) for f in frames]
	# 	list = ['Traceback (most recent call last):\n']
	# 	list += traceback.format_list(tb)
	# 	list += traceback.format_exception_only(self.exc_type, self.exc_value)
	# 	return list

	def get_traceback_frame_variables(self, tb_frame):

		return list(six.iteritems(tb_frame.f_locals))
