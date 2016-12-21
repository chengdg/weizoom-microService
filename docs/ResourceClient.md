# ResourceClient使用说明
---------------------------

## 1. 基本介绍

ResourceClient是访问其他服务中资源的方法。

`r = requests.get('https://api.github.com/user')`

使用requests包后，一行代码就能完成一次http请求，但是为了减轻业务代码处理各种情况的负担，就有了 APIResourceClient，它是调用外部微众服务的类，基于requests包，具有如下特性：
1. 支持调用restful形式的资源
2. 把各种错误信息封装在内部
3. 记录调用日志
4. 支持zipkin性能追踪
5. **不**支持调用第三方接口


## 2. 使用方法

```python

params = {
	'a':1,
	'b':2
}

from eaglet.utils.resource_client import Resource
resp = Resource.use('card').post({
	'resource': 'card.trade',
	'data': params
})
if resp:
	code = resp[code]
	# 处理业务成功
	if code ==200：
		...
	# 此时code为500，处理业务失败
	else:
		...
else:
	# 处理请求失败
	...
```

`Resource.use('card').post`支持get、put、post、delete方法。

### 2.1 参数

#### use参数
服务名称，如"card"。参见api-gateway项目。

#### resource
资源名称，如"card.trade"

#### data
请求的具体业务数据。**是一个可序列化的dict对象。**


### 2.2 返回值
一个典型的eaglet响应：

```
{
  "data": {
    "ship_infos": {}
  },
  "code": 200,
  "innerErrMsg": "",
  "errMsg": ""
}
```

格式及意义参见API Resource Response文档。当成功响应，即code为500或200时，**Resource会返回一个如上格式的dict对象**，否则返回None。


## 3. 日志说明

每次调用，都会记录type为call_service的watchdog日志，记录如下信息：
- is_success:是否为成功响应
- params:请求参数
- url：实际请求的url
- failure_type：失败类型，is_success为True则为空，否则有如下类型：
	- ServerResponseFailure：服务器返回非200响应、
	- ServiceProcessFailure：服务器返回200响应，但非成功响应（200、500）
	- requests.exceptions.RequestException中的各种类型
	- 其他可能的异常
- failure_msg：失败信息，堆栈信息或描述信息
- http_code：HTTP状态码，即resp.status_code
- resp_text:HTTP响应体，即resp.text

