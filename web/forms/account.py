#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: account.py
@time: 9/20/2020 5:11 PM
"""
from django import forms
from django_redis import get_redis_connection

from tarcker import settings
from web import models
from web.forms.bootstrap import BootStrapForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from utils.tencent.sendSms import sendMessage
from utils import encrypt
from tarcker.settings import apiId, apiKey
from tarcker.settings import sign, smsAppId


class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(label="密码", widget=forms.PasswordInput())
    confirmPassWord = forms.CharField(
        label="确认密码", widget=forms.PasswordInput()
    )
    mobilePhone = forms.CharField(
        label="手机号",
        validators=[
            RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$", "手机号格式错误"),
        ],
    )
    code = forms.CharField(label="验证码", widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        fields = [
            "username",
            "mail",
            "password",
            "confirmPassWord",
            "mobilePhone",
            "code",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = f"请输入{field.label}"

    def clean_username(self):
        """
        用户名校验
        """
        username = self.cleaned_data["username"]
        exist = models.UserInfo.objects.filter(username=username).exists()
        if exist:
            raise ValidationError("用户名已经存在")
        return username

    def clean_password(self):
        """
        确认密码并加密
        """
        password = self.cleaned_data["password"]

        return encrypt.md5(password)

    def clean_confirmPassWord(self):
        """
        密码确认校验
        """
        password = self.cleaned_data["password"]
        confirmPassWord = encrypt.md5(self.cleaned_data["confirmPassWord"])

        if password != confirmPassWord:
            raise ValidationError("两次密码不一致")
        return encrypt.md5(confirmPassWord)

    def clean_mobilePhone(self):
        """
        手机号校验钩子函数
        """
        mobilePhone = self.cleaned_data["mobilePhone"]
        # 判断手机号是否存在
        exits = models.UserInfo.objects.filter(
            mobilePhone=mobilePhone
        ).exists()
        if exits:
            raise ValidationError("手机号已经存在")
        return mobilePhone

    def clean_mail(self):
        """
        邮箱格式校验钩子函数
        """
        mail = self.cleaned_data["mail"]
        exists = models.UserInfo.objects.filter(mail=mail).exists()
        if exists:
            raise ValidationError("邮箱已存在")
        return mail

    def clean_code(self):
        code = self.cleaned_data["code"]

        # mobile_phone = self.cleaned_data['mobile_phone']

        mobile_phone = self.cleaned_data.get("mobilePhone")
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError("验证码失效或未发送，请重新发送")

        redis_str_code = redis_code.decode("utf-8")

        if code.strip() != redis_str_code:
            raise ValidationError("验证码错误，请重新输入")

        return code


class SendSmsForm(forms.Form):
    """
    发送短信
    """

    mobilePhone = forms.CharField(
        label="手机号",
        validators=[
            RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$", "手机号格式错误"),
        ],
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobilePhone(self):
        """
        手机号校验的钩子
        """
        mobilePhone = self.cleaned_data["mobilePhone"]
        print(mobilePhone)
        # 判断手机号是否存在
        exits = models.UserInfo.objects.filter(
            mobilePhone=mobilePhone
        ).exists()
        if exits:
            raise ValidationError("手机号已经存在")

        # 判断短信模板是否存在
        tpl = self.request.GET.get("tpl")
        templateId = settings.Tenct_Sms_Template[tpl]
        if not templateId:
            raise ValidationError("短信模板错误")

        # 发送短信
        smsClient = sendMessage(apiId, apiKey, sign, smsAppId)
        info = []
        if tpl == "register":
            sms = smsClient.send_message(
                ["+86" + mobilePhone], "713710", ["32124"]
            )
            info.append(sms.get("Code"))
            info.append("713710")
        elif tpl == "login":
            sms = smsClient.send_message(
                ["+86" + mobilePhone], "713711", ["19284", "1"]
            )
            info.append(sms.get("Code"))
            info.append("713710")
        else:
            sms = smsClient.send_message(
                ["+86" + mobilePhone], "713711", ["32435"]
            )
            info.append(sms.get("Code"))
            info.append("713710")
        # 发送短信
        if info[0] != "Ok":
            raise ValidationError(f"短信发送失败，{info[0]}")

        # 验证码 写入redis（django-redis）
        conn = get_redis_connection()
        conn.set(mobilePhone, info[1], ex=60)

        return mobilePhone


class LoginSMSForm(BootStrapForm, forms.Form):
    mobilePhone = forms.CharField(
        label="手机号",
        validators=[
            RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$", "手机号格式错误"),
        ],
    )

    code = forms.CharField(label="验证码", widget=forms.TextInput())

    def clean_mobile_phone(self):
        mobilePhone = self.cleaned_data["mobilePhone"]
        exists = models.UserInfo.objects.filter(
            mobilePhone=mobilePhone
        ).exists()
        if not exists:
            raise ValidationError("手机号不存在")

        return mobilePhone

    def clean_code(self):
        code = self.cleaned_data["code"]
        mobile_phone = self.cleaned_data.get("mobile_phone")

        # 手机号不存在，则验证码无需再校验
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)  # 根据手机号去获取验证码
        if not redis_code:
            raise ValidationError("验证码失效或未发送，请重新发送")

        redis_str_code = redis_code.decode("utf-8")

        if code.strip() != redis_str_code:
            raise ValidationError("验证码错误，请重新输入")

        return code


class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label="邮箱或手机号")
    password = forms.CharField(
        label="密码", widget=forms.PasswordInput(render_value=True)
    )
    code = forms.CharField(label="图片验证码")

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        # 加密 & 返回
        return encrypt.md5(pwd)

    def clean_code(self):
        """ 钩子 图片验证码是否正确？ """
        # 读取用户输入的yanzhengm
        code = self.cleaned_data["code"]

        # 去session获取自己的验证码
        session_code = self.request.session.get("image_code")
        if not session_code:
            raise ValidationError("验证码已过期，请重新获取")

        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError("验证码输入错误")

        return code
