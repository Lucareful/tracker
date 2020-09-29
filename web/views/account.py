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
    form = RegisterModelForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        return render(request, 'register.html', {'form': form})
    print(request.POST)

    return JsonResponse({'status': False, 'error': form.errors})


def sendSms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return HttpResponse('成功')
