#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: urls.py
@time: 9/19/2020 2:24 PM
"""

from django.urls import path, include
from django.conf.urls import url
from web.views import account, home, project

urlpatterns = [
    url(r"^register/$", account.register, name="register"),
    url(r"^login/sms/$", account.login_sms, name="login_sms"),
    url(r"^login/$", account.login, name="login"),
    url(r"^image/code/$", account.image_code, name="image_code"),
    url(r"^send/sms/$", account.sendSms, name="send_sms"),
    url(r"^index/$", home.index, name="index"),
    url(r"^logout/$", account.logout, name="logout"),
    # 项目列表
    url(r"^project/list/$", project.project_list, name="project_list"),
]
