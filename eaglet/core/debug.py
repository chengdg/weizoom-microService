# -*- coding: utf-8 -*-
import os
import re
from collections import OrderedDict
import six
from decimal import Decimal
import datetime
import traceback
import sys


def get_req_data(req):
	return req.params


def full_stack():
	exc = sys.exc_info()[0]
	stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
	if not exc is None:  # i.e. if an exception is present
		del stack[-1]  # remove call of full_stack, the printed exception
	# will contain the caught exception caller instead
	trc = 'Traceback (most recent call last, REVERSED CALL ORDER):\n'
	stackstr = trc + ''.join(reversed(traceback.format_list(stack)))
	if not exc is None:
		stackstr += '  ' + traceback.format_exc().lstrip(trc)

	return stackstr


def unicode_full_stack():
	return full_stack().decode('utf-8')


def get_uncaught_exception_data(req):
	reporter = ExceptionReporter(*sys.exc_info())
	try:
		exception_data = reporter.get_exception_data()
	except:
		exception_data = unicode_full_stack()
	data = OrderedDict((
		('exception_id', reporter.exception_id),
		('req_data', get_req_data(req)),
		('exception_data', exception_data),
		('traceback', unicode_full_stack()),
	))
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
			# Note: We extension .decode() here, instead of six.text_type(s, encoding,
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

	def __init__(self, exc_type, exc_value, tb):
		self.exc_type = exc_type
		self.exc_value = exc_value
		self.tb = tb

		self.loader_debug_info = None

		# Handle deprecated string exceptions
		if isinstance(self.exc_type, six.string_types):
			self.exc_value = Exception('Deprecated String Exception: %r' % self.exc_type)
			self.exc_type = type(self.exc_value)

		self.exception_id = ''

	def format_path_status(self, path):
		if not os.path.exists(path):
			return "File does not exist"
		if not os.path.isfile(path):
			return "Not a file"
		if not os.access(path, os.R_OK):
			return "File is not readable"
		return "File exists"

	def _get_bussines_data(self, tb):

		vars = list(six.iteritems(tb.tb_frame.f_locals))
		vars = [{'key': k, 'value': v} for k, v in vars if
		        (not k.startswith("__") and not k.endswith("__") and k != 'response')]
		print(vars)
		try:
			import debug_handler
			data = debug_handler.handle(vars)
		except:
			data = {}

		return data

	def get_exception_data(self):
		"Return a Context instance containing traceback information."

		frames, last_tb = self.get_traceback_frames()
		for i, frame in enumerate(frames):
			if 'vars' in frame:
				frame['vars'] = [{'key': k, 'value': force_text(v)} for k, v in frame['vars'] if
				                 (not k.startswith("__") and not k.endswith("__") and k != 'response')]
			frames[i] = frame

		# unicode_hint = ''
		# if self.exc_type and issubclass(self.exc_type, UnicodeError):
		# 	start = getattr(self.exc_value, 'start', None)
		# 	end = getattr(self.exc_value, 'end', None)
		# 	if start is not None and end is not None:
		# 		unicode_str = self.exc_value.args[1]
		# 		unicode_hint = smart_text(unicode_str[max(start - 5, 0):min(end + 5, len(unicode_str))], 'ascii',
		# 		                          errors='replace')
		bussines_data = {}
		if last_tb:
			bussines_data = self._get_bussines_data(last_tb)

		system_info = OrderedDict((
			('sys_executable', sys.executable),
			('sys_version_info', ('%d.%d.%d' % sys.version_info[0:3])),
			('server_time', str(datetime.datetime.now()))
			# ('sys_path', sys.path)

		))

		last_frame = frames[-1]

		self.exception_id = last_frame['filename'] + '-' + str(last_frame['lineno'])

		summary = OrderedDict((
			('exception_type', self.exc_type.__name__ if self.exc_type else ''),
			('exception_value', smart_text(self.exc_value, errors='replace') if self.exc_value else ''),
			('filename', last_frame['filename']),
			('line', last_frame['context_line']),
			('lineno', last_frame['lineno']),
			('bussines_data', bussines_data)
		))

		c = OrderedDict((
			('summary', summary),
			('system_info', system_info),
			('frames', frames)
		))
		# Check whether exception info is available

		c['frames'] = frames

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
		last_tb = tb
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
			frames.append(OrderedDict([
				# 'tb': tb,
				('filename', filename),
				('function', function),
				('vars', self.get_traceback_frame_variables(tb.tb_frame)),
				# ('pre_context', pre_context),
				('lineno', tb.tb_lineno),
				('context_line', context_line.replace("\t", "    ")),
				# ('post_context', post_context),
			]))
			last_tb = tb
			tb = tb.tb_next

		return frames, last_tb

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
