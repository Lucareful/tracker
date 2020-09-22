#!/usr/bin/env python
# encoding: utf-8
'''
@author: Luenci
@file: urls.py
@time: 9/19/2020 2:24 PM
'''

from django.urls import path, include
from web.views import account


urlpatterns = [
    # path('sms', include('web.urls')),
    path(r'register/', account.login),
    path(r'send/sms/', account.sendSms),
]
