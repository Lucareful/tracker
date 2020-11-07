#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: auth.py
@time: 10/17/2020 12:53 PM
"""
import arrow
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from web import models


class Tracker(object):
    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None


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

        request.tracker = Tracker()
        user_id = request.session.get("user_id", 0)
        print("session:", request.session)
        print("user_id:", user_id)
        user_project = models.UserInfo.objects.filter(id=user_id).first()

        request.tracker.user = user_project

        # 获取url白名单,校验路由
        if request.path_info in settings.WHITE_URL_LIST:
            return None

        # 判断用户是否登录
        if not request.tracker.user:
            return redirect("login")

        # 登录成功之后，获取用户的所拥有的额度
        _object = (
            models.Transaction.objects.filter(user=user_project, status=2)
            .order_by("-id")
            .first()
        )
        # 额度时间判断
        current_datetiem = arrow.now()
        if _object.end_datetime and _object.end_datetime < current_datetiem:
            _object = models.Transaction.objects.filter(
                user=user_project, price_policy__category=1
            ).first()

        request.tracker.price_policy = _object.price_policy
