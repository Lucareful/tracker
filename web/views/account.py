#!/usr/bin/env python
# encoding: utf-8
'''
@author: Luenci
@file: account.py
@time: 9/18/2020 10:27 PM
'''

from django.shortcuts import render


def login(request):
    return render(request, 'register.html')
