from django.db import models


# Create your models here.

class UserInfo(models.Model):
    """
    用户信息model
    """
    username = models.CharField(max_length=66, verbose_name='用户名')
    password = models.CharField(max_length=66, verbose_name='密码')
    mail = models.EmailField(max_length=66, verbose_name='邮箱')
    mobilePhone = models.CharField(max_length=66, verbose_name='手机号')
