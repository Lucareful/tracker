#!/usr/bin/env python
# encoding: utf-8
'''
@author: Luenci
@file: urls.py
@time: 9/19/2020 2:24 PM
'''

from django.urls import path, include

urlpatterns = [
    path('sms', include('web.urls')),
]
