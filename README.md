**eaglet —— Python微服务核心框架**

eaglet为开发python微服务提供了核心框架，每一个python微服务都使用eaglet进行开发。eaglet对于微服务的价值，类似于Django对于web开发的价值。

## 安装 ##
执行：
```
pip install git+https://git2.weizzz.com:84/microservice/eaglet.git
```

## 更新

```
pip install -U git+https://git2.weizzz.com:84/microservice/eaglet.git
```

## 安装指定分支、tag、commit
```
git+https://git2.weizzz.com:84/microservice/eaglet.git@master
git+https://git2.weizzz.com:84/microservice/eaglet.git@v1.0
git+https://git2.weizzz.com:84/microservice/eaglet.git@da39a3ee5e6b4b0d3255bfef95601890afd80709
```

## 如何使用 ##
使用geser生成微服务的codebase

## 集成mongo ##
在项目setting中配置：
```
DATABASES = {
    ...
    'apps_default': {
        'ENGINE': 'mongo',                 # used MongoDB
        'NAME': 'app_data',                # DATABASE NAME
        'USER': None,                      # USERNAME
        'PASSWORD': None,                  # PASSWORD
        'HOST': 'mongo.apps.com',          # HOST
        "ALIAS": 'apps',                   # ALIAS
        "PORT": 27017                      # PROT
    }
    ....
}
```


## 分布式celery：send_task ##

**应用场景**
消息模版需求：积分变动发送模版消息。目前微服务场景下，member_service，apiserver,zeus都会修改会员积分，所有使用消息队列方式，解决模版消息业务侵入各独立service。
接下缓存策略中缓存更新也将使用异步消息的方式。

**用法**：

    from eaglet.core.utils.send_task import send_task

    send_task(queue_name, args)

**说明**：

    <queue_name> : 服务(队列名称)的名称。

**用法举例**：
    
    integarl_log = {
        "member_id":1,
        "nick_name":"weizoom",
        "event_type": "好友通过分享链接购买商品",
        "increase_integral": 100,
        "current_integral": 200
    }
    send_task("services.template_message_integral_service.tasks.service_tempate_message_integral", integarl_log)


# 启动API授权机制

1. **API service端**：为API Resource method增加 `@access_token_required()`。例如：
```
from api.decorators import access_token_required

class AData(api_resource.ApiResource):
    app = 'demo'
    resource = 'data'

    @param_required(['id'])
    @access_token_required() # <--- 增加decorator
    def get(args):
        // ...
        return {
            "args": args
        }
```

2. **Client端**：在settings中加上
```
ENABLE_API_AUTH = True
APP_KEY = '<对应的app key>'
APP_SECRET = '<对应的secret>'
```

## API授权访问流程

1. 在`Hermes`中调用`Resource.use()`；
2. `eaglet.utils.resource_client.Resource` 向API service申请access_token（需要app_key和app_secret）；
3. Hermes中获得的client再访问API时会加上access_token。

## TODO

需要将`resource_client.py`独立成一个插件，加上缓存access_token的DB Model。
