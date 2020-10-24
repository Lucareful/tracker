#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: auth.py
@time: 10/17/2020 12:53 PM
"""
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from web import models


class AuthMiddleware(MiddlewareMixin):
    """
    用户认证中间件
    """

    def process_request(self, request):
        """
        判断用户是否登录.
        :param request:
        :return:
        """
        user_id = request.session.get("user_id", 0)
        print("session:", request.session)
        print("user_id:", user_id)
        user_obj = models.UserInfo.objects.filter(id=user_id).first()
        request.tracker = user_obj

        # 判断用户是否登录
        if not request.tracker:
            return redirect("login")
