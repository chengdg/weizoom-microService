eaglet框架的return
-------------------------------

```
class AShipInfo(api_resource.ApiResource):
	"""
	收货地址
	"""
	app = 'mall'
	resource = 'ship_info'

	@param_required(['ship_id'])
	def delete(args):
		"""
		删除收货地址
		@param ship_id
		@return 删除后的默认地址

		"""
		webapp_user = args['webapp_user']
		selected_id = webapp_user.delete_ship_info(args['ship_id'])
		return {
			'selected_id': selected_id
		}

```

## 序列化

在微服务通信中，使用json（Content-Type：application/json）作为标准数据格式，也就需要服务能够把自己的数据序列化成json，并能反序列化json成自己的数据。

- 序列化： 将数据结构或对象转换成二进制串的过程。
- 反序列化：将在序列化过程中所生成的二进制串转换成数据结构或者对象的过程。

在python中，使用标准库`json`操作。`json.dumps()`把python dict对象序列化成json字符串，`json.loads()`把json字符串反序列化成python dict对象。


## eaglet中的序列化

eaglet框架发出的HTTP response是json（Content-Type	application/json; charset=utf-8）格式的，序列化操作（即json.dumps）是eaglet框架做的（eaglet/apps.py call_wapi方法中的resp.body = json.dumps(response, default=_default)），开发者需要在ROA资源（即api层各方法的return）返回**可序列化的对象**。 **注：**准确说是dict对象，即使不是dict，而仅仅是一个字符串在语法及eaglet框架功能上都是支持的，但是我们约定内容是字典格式的，而不是一个简单的数字、字符串。


### 可序列化对象

JSON和Python内置的数据类型对应如下：

|  JSON类型 |  Python类型 
|---|---|
|  {} |  dict |
|  [] |   list|
|   "string"| 'str'或u'unicode'  |
|1234.56|int或float|
|true/false|True/Fasle|
|null|None|

以上就是可序列化的类型，dict、list中的值也必须是可序列化的。

而一个class的示例对象是不能**直接**序列化的，会产生异常：
>Traceback (most recent call last):
  ...
TypeError: <__main__.Student object at 0x10aabef50> is not JSON serializable

在eaglet中，使用`json.dumps(response, default=_default)`中的`_default`函数支持，支持`datetime.datetime`、`datetime.data`、`decimal.Decimal`自动转为字符串。对于特定类型的python对象，自然特定的方法提取其内容转成可序列化的数据，但这就不是eaglet框架做的了，框架不会去支持特定业务。

BUG 9094是因为在api层返回了一个apiserver中的bussine.model,临时解决方法是调用这个bussine.model的to_dict方法。现在BUG 9094已经解决，但是考虑到基于eaglet都有bussine.model，而开发中如若不慎，可能直接返回。在eaglet去除上述特定支持后，这么返回必然报错。
