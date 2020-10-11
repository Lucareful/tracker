#!/usr/bin/env python
# encoding: utf-8
'''
@author: Luenci
@file: account.py
@time: 9/20/2020 5:11 PM
'''
import random
import hashlib

from django import forms

from tarcker import settings
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from utils.tencent.sendSms import sendMessage
from tarcker.settings import apiId, apiKey
from tarcker.settings import sign, smsAppId


class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput()
    )
    confirmPassWord = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput()
    )
    mobilePhone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput()
    )

    class Meta:
        model = models.UserInfo
        fields = ['username', 'mail', 'password', 'confirmPassWord', 'mobilePhone', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = f'请输入{field.label}'

    def clean_username(self):
        """
        用户名校验
        """
        username = self.cleaned_data['username']
        exist = models.UserInfo.objects.filter(username=username).exists()
        if exist:
            raise ValidationError('用户名已经存在')
        return username

    def clean_password(self):
        """
        确认密码并加密
        """
        password = self.cleaned_data['password']

        return hashlib.md5(password.encode('utf-8'))

    def clean_confirmPassWord(self):
        """
        密码确认校验
        """
        password = self.cleaned_data['password']
        confirmPassWord = self.cleaned_data['confirmPassWord']

        if password.hexdigest() != hashlib.md5(confirmPassWord.encode('utf-8')).hexdigest():
            raise ValidationError('两次密码不一致')
        return hashlib.md5(confirmPassWord.encode('utf-8'))

    def clean_mobilePhone(self):
        """
        手机号校验钩子函数
        """
        mobilePhone = self.cleaned_data['mobilePhone']
        # 判断手机号是否存在
        exits = models.UserInfo.objects.filter(mobilePhone=mobilePhone).exists()
        if exits:
            raise ValidationError('手机号已经存在')
        return mobilePhone

    def clean_mail(self):
        """
        邮箱格式校验钩子函数
        """
        mail = self.cleaned_data['mail']
        exists = models.UserInfo.objects.filter(mail=mail).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return mail


class SendSmsForm(forms.Form):
    """
    发送短信
    """
    mobilePhone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobilePhone(self):
        """
        手机号校验的钩子
        """
        mobilePhone = self.cleaned_data['mobilePhone']
        print(mobilePhone)
        # 判断手机号是否存在
        exits = models.UserInfo.objects.filter(mobilePhone=mobilePhone).exists()
        if exits:
            raise ValidationError('手机号已经存在')

        # 判断短信模板是否存在
        tpl = self.request.GET.get('tpl')
        templateId = settings.Tenct_Sms_Template[tpl]
        if not templateId:
            raise ValidationError('短信模板错误')

        # 发送短信
        smsClient = sendMessage(apiId, apiKey, sign, smsAppId)
        code = random.randrange(10000, 99999)
        if tpl == 'register':
            sms = smsClient.send_message(['+86' + mobilePhone], '713710', ['32124'])
        elif tpl == 'login':
            sms = smsClient.send_message(['+86' + mobilePhone], '713711', ['19284', '1'])
        else:
            sms = smsClient.send_message(['+86' + mobilePhone], '713711', ['32435'])
        return sms
