# eaglet日志介绍
## Web框架日志
### CALL_API
类型：CALL_API  
含义：记录**接收**的HTTP请求请求参数和响应内容  
是否使用watchdog： 是  
格式：
```
"app":"",	# app
"resource":"",	# resource
"method":"",	# get/post/put/delete
"req_params":"",	# 请求参数
"response"	# 响应内容
```

### Uncaught_Exception
类型：Uncaught_Exception  
含义：当发生未捕获异常时，会记录异常信息  
是否使用watchdog： 是  
格式：
```
"exception_id"：“” # 以文件路径和报错行数标记的id
"req_data":""	# 请求参数
"exception_data":	# 异常数据
	{
		"summary":	# 概要
		{
			"exception_type":	# 异常类型
			"exception_value": # 异常值
			"filename"： # 	文件路径
			"line":	"	# 该行代码
			"lineno": # 行数
			"bussines_data"		# 加载项目中debug_handler.handle函数返回的数据，如果没有则为空/
		},
        “system_info”:
        {
            "sys_executable":"",
            "sys_version_info": ""	# python版本
            “server_time”:	"" # 系统时间
        },
        "frames":	# 堆栈信息，从上到下按顺序显示每一帧
        [
            {
                "filename": # 文件路径
                "function":
                "vars":		# 变量信息
                {
                    "key":,
                    "value"
                },
                "lineno":"",
                "context_line",
            },
            ...
        ]
	}，
"traceback":{}
    
```


### zipkin
含义：记录zipkin的性能追踪日志。  
是否使用watchdog： 否

## 工具组件日志
### Resource
记录**发送**的HTTP请求请求参数和响应内容  
是否使用watchdog： 是


见 <https://git2.weizzz.com:84/microservice/eaglet/blob/master/docs/ResourceClient.md#3-%E6%97%A5%E5%BF%97%E8%AF%B4%E6%98%8E>



--------------

参考：[日志系统日志规范](https://git2.weizzz.com:84/kbase/kbase/blob/master/dev_ops/ELK_log_collection_standard.md#L1)