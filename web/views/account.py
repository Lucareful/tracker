#!/usr/bin/env python
# encoding: utf-8
'''
@author: Luenci
@file: account.py
@time: 9/18/2020 10:27 PM
'''

from django.shortcuts import render, HttpResponse
from web.forms.account import RegisterModelForm, SendSmsForm


def login(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})


def sendSms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        pass
    return HttpResponse('成功')
