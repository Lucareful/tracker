#!/usr/bin/env python
# encoding: utf-8
'''
@author: Luenci
@file: account.py
@time: 9/18/2020 10:27 PM
'''

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from web.forms.account import RegisterModelForm, SendSmsForm


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    form = RegisterModelForm(request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 通过验证，数据写入
        instance = form.save()
        return render(request, 'register.html', {'form': form})
    print(request.POST)

    return JsonResponse({'status': False, 'error': form.errors})


def sendSms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})
