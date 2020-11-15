#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: .py
@time: 10/24/2020 11:26 AM
"""

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from web import models
from web.forms.project import ProjectModelForm


def project_list(request):
    print(request.tracker.user)
    if request.method == "GET":
        project_dict = {"star": [], "my": [], "join": []}
        # 我创建的所有项目
        my_project_list = models.Project.objects.filter(
            creator=request.tracker.user
        )
        for row in my_project_list:
            if row.star:
                project_dict["star"].append({"value": row, "type": "my"})
            else:
                project_dict["my"].append(row)

        # 我参与的所有项目
        join_project_list = models.ProjectUser.objects.filter(
            user=request.tracker.user
        )
        for item in join_project_list:
            if item.star:
                project_dict["star"].append(
                    {"value": item.project, "type": "join"}
                )
            else:
                project_dict["my"].append(item.project)

        form = ProjectModelForm(request)
        return render(
            request,
            "project_list.html",
            {"form": form, "project_dict": project_dict},
        )
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        # 将项目制定为当前登录的用户
        form.instance.creator = request.tracker.user
        # 保存项目
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def project_star(request, project_type, project_id):
    """
    星标项目
    :param request:
    :param project_type:
    :param project_id:
    :return:
    """
    if project_type == "my":
        models.Project.objects.filter(
            id=project_id, creator=request.tracker.user
        ).update(star=True)
        return redirect("project_list")
    elif project_type == "join":
        models.ProjectUser.objects.filter(
            project_id=project_id, user=request.tracker.user
        ).update(star=True)
        return redirect("project_list")

    return HttpResponse("请求错误")


def project_unstar(request, project_type, project_id):
    """
    取消星标项目
    :param request:
    :param project_type:
    :param project_id:
    :return:
    """
    if project_type == "my":
        models.Project.objects.filter(
            id=project_id, creator=request.tracker.user
        ).update(star=False)
        return redirect("project_list")
    elif project_type == "join":
        models.ProjectUser.objects.filter(
            project_id=project_id, user=request.tracker.user
        ).update(star=False)
        return redirect("project_list")

    return HttpResponse("请求错误")
