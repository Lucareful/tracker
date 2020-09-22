#!/usr/bin/env python
# encoding: utf-8
'''
@author: Luenci
@file: account.py
@time: 9/20/2020 5:11 PM
'''
from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class RegisterModelForm(forms.ModelForm):
    mobilePhone = forms.CharField(label='手机号', validators=[RegexValidator(r'\d{3}-\d{8}|\d{4}-\d{7}', '手机号格式错误'), ])
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput()
    )
    confirmPassWord = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput()
    )
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


class SendSmsForm(forms.Form):
    """
    发送短信
    """
    mobilePhone = forms.CharField(label='手机号', validators=[RegexValidator(r'\d{3}-\d{8}|\d{4}-\d{7}', '手机号格式错误'), ])

    def clean_mobilePhone(self):
        """
        手机号校验的钩子
        """
        mobilePhone = self.cleaned_data['mobilePhone']
        exits = models.UserInfo.objects.filter(mobilePhone=mobilePhone).exists()
        if exits:
            raise ValidationError()
