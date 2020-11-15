#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: project.py
@time: 11/7/2020 9:39 AM
"""

from django import forms
from django.core.exceptions import ValidationError
from web.forms.bootstrap import BootStrapForm
from web import models
from web.forms.widgest import ColorRadioSelect


class ProjectModelForm(BootStrapForm, forms.ModelForm):
    bootstrap_class_exclude = ["color"]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = models.Project
        fields = ["name", "color", "desc"]
        # 字段重写
        widgets = {
            "desc": forms.Textarea,
            "color": ColorRadioSelect(attrs={"class": "color-radio"}),
        }

    def clean_name(self):
        """
        钩子函数校验项目
        :return:
        """
        name = self.cleaned_data["name"]
        user = self.request.tracker.user
        # 1.校验当前用户创建的项目是否存在
        exists = models.Project.objects.filter(
            name=name, creator=user
        ).exists()
        if exists:
            raise ValidationError("项目名称已经存在")
        # 2.校验当前用户是否有足够的项目额度
        # 当前用户拥有的项目个数额度
        maxProjectNum = self.request.tracker.price_policy.project_num
        # 当前用户已经创建的项目个数
        currentProjectNum = models.Project.objects.filter(creator=user).count()
        if currentProjectNum >= maxProjectNum:
            raise ValidationError("您项目额度已用完，无法创建更多的项目")
        return name
