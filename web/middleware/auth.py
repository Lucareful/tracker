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

    def process_view(self, request, view, args, kwargs):
        """
        判断路由是否是以 manage 开头
        :param request:
        :param view:
        :param args:
        :param kwargs:
        :return:
        """
        if not request.path_info.startswith("/manage/"):
            return
        # print(view)
        # print(args)
        # print(kwargs)
        project_id = kwargs.get("project_id")
        user = request.tracker.user

        # 是否是当前用户创建的项目
        project_object = models.Project.objects.filter(
            creator=user, id=project_id
        ).first()
        if project_object:
            # 是我创建的项目的话，我就让他通过
            request.tracker.project = project_object
            return None

        # 是否是我参与的项目
        project_user_object = models.ProjectUser.objects.filter(
            user=user, project_id=project_id
        ).first()
        if project_user_object:
            # 是我参与的项目
            request.tracker.project = project_user_object.project
            return None

        return redirect("project_list")
