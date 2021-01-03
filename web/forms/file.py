#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: file.py
@time: 1/3/2021 1:47 PM
"""
from django import forms
from django.core.exceptions import ValidationError
from web.forms.bootstrap import BootStrapForm
from web import models

from utils.tencent.cos import check_file


class FolderModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.FileRepository
        fields = ["name"]

    def __init__(self, request, parent_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.parent_object = parent_object

    def clean_name(self):
        name = self.cleaned_data["name"]

        # 数据库判断 当前目录 下此 文件夹是否已存在
        queryset = models.FileRepository.objects.filter(
            file_type=2, name=name, project=self.request.tracker.project
        )
        if self.parent_object:
            exists = queryset.filter(parent=self.parent_object).exists()
        else:
            exists = queryset.filter(parent__isnull=True).exists()
        if exists:
            raise ValidationError("文件夹已存在")
        return name


class FileModelForm(forms.ModelForm):
    etag = forms.CharField(label="ETag")

    class Meta:
        model = models.FileRepository
        exclude = ["project", "file_type", "update_user", "update_datetime"]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_file_path(self):
        return "https://{}".format(self.cleaned_data["file_path"])
