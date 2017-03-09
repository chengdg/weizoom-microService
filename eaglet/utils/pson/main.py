# -*- coding: UTF-8 -*-

from eaglet.utils.pson import utils


def dumps(data, stringify=True):
	result = utils.get_path_value(data, stringify=stringify)
	return ",,".join(result)


def loads(data):
	change = utils.parse(data)
	result = utils.patch({}, change)
	return result
