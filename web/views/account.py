#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: account.py
@time: 9/18/2020 10:27 PM
"""
from io import BytesIO
import uuid
import arrow
from utils.ImgCode import check_code
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

from web import models
from web.forms.account import (
    RegisterModelForm,
    SendSmsForm,
    LoginSMSForm,
    LoginForm,
)
from django.db.models import Q


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, "register.html", {"form": form})

    form = RegisterModelForm(request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 通过验证，数据写入(用户表中插入一条数据)
        instance = form.save()
        # 创建免费的交易记录
        policy_obj = models.PricePolicy.objects.filter(
            category=1, title="个人免费版"
        ).first()
        models.Transaction.objects.create(
            status=2,
            order=str(uuid.uuid4()),
            user=instance,
            price_policy=policy_obj,
            start_datetime=arrow.now(),
        )
        return JsonResponse({"status": True, "data": "/login/"})

    return JsonResponse({"status": False, "error": form.errors})


def sendSms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def login_sms(request):
    """ 短信登录 """
    if request.method == "GET":
        form = LoginSMSForm()
        return render(request, "login_sms.html", {"form": form})
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        # 用户输入正确，登录成功
        mobile_phone = form.cleaned_data["mobile_phone"]

        # 把用户名写入到session中
        user_object = models.UserInfo.objects.filter(
            mobile_phone=mobile_phone
        ).first()
        request.session["user_id"] = user_object.id
        request.session.set_expiry(59 * 60 * 24 * 14)

        return JsonResponse({"status": True, "data": "/index/"})

    return JsonResponse({"status": False, "error": form.errors})


def login(request):
    """ 用户名和密码登录 """
    if request.method == "GET":
        form = LoginForm(request)
        return render(request, "login.html", {"form": form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user_object = (
            models.UserInfo.objects.filter(
                Q(mail=username) | Q(mobilePhone=username)
            )
            .filter(password=password)
            .first()
        )
        if user_object:
            # 登录成功为止0
            request.session["user_id"] = user_object.id
            request.session.set_expiry(59 * 60 * 24 * 14)

            return redirect("index")

        form.add_error("username", "用户名或密码错误")

    return render(request, "login.html", {"form": form})


def image_code(request):
    """ 生成图片验证码 """

    image_object, code = check_code()

    request.session["image_code"] = code
    # 主动修改session的过期时间为59s
    request.session.set_expiry(59)

    stream = BytesIO()
    image_object.save(stream, "png")
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect("index")
