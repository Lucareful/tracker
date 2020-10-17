# 一个基于Django的bug追踪和任务管理平台
> 参考哔哩哔哩视频：https://www.bilibili.com/video/BV1uA411b77M
> gittee:https://gitee.com/wupeiqi/s25
## 腾讯云短信接口
### 提供功能
- 注册验证码
- 登录验证码
- 密码重置验证码
### 实现步骤
官方文档：https://cloud.tencent.com/document/product/382/43196
- 安装腾讯云短信的SDK
```shell
 pip install tencentcloud-sdk-python
```
## Django-redis
- django-redis的使用
```python
# django-redis 配置
CACHES = {
    'default': { # 默认配置
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100,#最大连接数
                'encoding': 'utf-8',
            },
            'PASSWORD': "密码",
        }
    }
}
```
## 登录，注册model开发完成

![image-20201017134243289](https://gitee.com/luenci/RepoImg/raw/master/img/image-20201017134243289.png)
