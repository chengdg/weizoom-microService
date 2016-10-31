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


def param_required(params=None):
    """用于检查函数参数的decorator

    1. name,表示为必须参数
    2. name:type,表示自动类型转换，支持"str","int","float","bool","json"。其中bool识别True/False,"True"/"False","true"/"false"
    3. ?name,以?开头的参数，表示非必须参数

    ```
    @param_required(['id', 'name'])
    def name(self):
        return 'hello ' + 'world'
    ```
    """

    def wrapper(function):
        def inner(data):
            for param in params:
                if ':' in param:
                    param_name, param_type = param.split(':')
                else:
                    param_name = param
                    param_type = None
                if '?' in param_name:
                    param_name = param_name.replace('?', '')
                    is_required = False
                else:
                    is_required = True

                if is_required and param_name not in data:
                    raise ApiParamaterError('Required parameter missing: %s' % param_name)

                try:

                    if param_type and param_name in data:
                        param_value = data[param_name]
                        if param_type == "int":
                            data[param_name] = int(param_value)
                        elif param_type == 'bool':
                            data[param_name] = param_value in ("True", "true", True)
                        elif param_type == "float":
                            data[param_name] = float(param_value)
                        elif param_type == "json":
                            data[param_name] = json.loads(param_value)
                except BaseException as e:
                    raise ApiParamaterError('Invalid parameter: %s is not %s.%s' % (param_name, param_type, e.message))

            return function(data)

        return inner

    return wrapper
