**eaglet —— Python微服务核心框架**

eaglet为开发python微服务提供了核心框架，每一个python微服务都使用eaglet进行开发。eaglet对于微服务的价值，类似于Django对于web开发的价值。

## 安装 ##
执行：
```
pip install git+https://git2.weizzz.com:84/microservice/eaglet.git
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
