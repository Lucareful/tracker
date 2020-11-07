#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: project.py
@time: 10/24/2020 11:26 AM
"""

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from web.forms.project import ProjectModelForm


def project_list(request):
    print(request.tracker.user)
    if request.method == "GET":
        form = ProjectModelForm(request)
        return render(request, "project_list.html", {"form": form})
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        # 将项目制定为当前登录的用户
        form.instance.creator = request.tracker.user
        # 保存项目
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})
