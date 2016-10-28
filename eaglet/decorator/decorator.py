# -*- coding: utf-8 -*-
import json


class cached_context_property(object):
    """用于指定一个可以被context缓存的decorator

    ```
    @cached_context_property
    def name(self):
    	return 'hello ' + 'world'
    ```

    当我们调用`self.name`之后，`self.context['name'] = 'hello world'`，后续访问`self.name`，会直接从`self.context`中获取
    """
    def __init__(self, func):
        self.func = func
        self.func_name = func.__name__

    def __get__(self, instance, type=None):
        if instance is None:
            return self

        value = instance.context.get(self.func_name, None)
        if not value:
        	value = self.func(instance)
        	instance.context[self.func_name] = value
        return value


class ApiParamaterError(Exception):
    pass


# Reference: http://swagger.io/specification/#dataTypeType
SWAGGER_TYPE2PYTHON_TYPE = {
    'integer': int,
    'number': float,
    'string': str,
    # 'boolean':'', bool值单独处理
}


def param_required(params=None):
    """用于检查函数参数的decorator
    兼容
    ```
    @param_required(['id', 'name'])
    def name(self):
        return 'hello ' + 'world'
    ```
    `
    此时参数为必须参数，不做其他处理。

    推荐使用swagger形式：
    ```
    @param_required([{
		'name': 'id',
		'type': 'integer',
		'required': True
	}, {
		'name': 'xx',
		'type': 'string',
		'format': 'json'
		'required':False
	}])
	def get(args):
    ```

    类型(type)必须为：
        - integer
        - number
        - string
        - boolean:识别True/False,"True"/"False","true"/"false"
    格式(format)支持:
        - 当type为string时，支持'json'的格式化

    """

    def wrapper(function):
        def inner(data):
            for param in params:
                if isinstance(param, basestring):
                    param_name = param
                    param_type = None
                    param_format = None
                    required = True
                else:
                    param_name = param['name']
                    param_type = param.get('type')  # 默认不检测类型
                    param_format = param.get('format')  # 默认不进行格式化
                    required = param.get('required', True) in (True, 'true')  # 默认为必须值
                if required and param_name not in data:
                    raise ApiParamaterError('Required parameter missing: %s' % param)
                if param_type:
                    param_value = data[param_name]
                    if param_type in SWAGGER_TYPE2PYTHON_TYPE:
                        try:

                            data[param_name] = SWAGGER_TYPE2PYTHON_TYPE[param_type](param_value)
                        except BaseException as e:

                            raise ApiParamaterError(
                                'Parameter {} is not {}.GET {}'.format(param_name, param_type, type(data[param_name])))
                    elif param_type == 'boolean':
                        if param_value not in ['true', 'True', True]:
                            raise ApiParamaterError(
                                'Parameter {} is not {}.GET {}'.format(param_name, param_type, type(data[param_name])))
                    else:
                        raise ApiParamaterError(
                            'Parameter {} is requested invalid type:{}'.format(param_name, param_type))
                if param_format:
                    if param_format == 'json':
                        try:
                            data[param_name] = json.loads(data[param_name])
                        except:
                            raise ApiParamaterError(
                                'Parameter {} is invalid format. Required {}'.format(param_name, param_format))
            return function(data)

        return inner

    return wrapper
