#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: offlineScript.py
@time: 10/17/2020 5:38 PM
"""
import os
import django
import importlib
import argparse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tarcker.settings")
django.setup()


def models():
    # 参数解析
    # 输入 python offlineScript.py web.tests.test
    parser = argparse.ArgumentParser(description="Description of this script.")
    parser.add_argument("--model", dest="model", required=True, type=str)
    modelNamespace = parser.parse_args()

    # 将modelPath分割，最后一个.后面的应该是执行的函数
    tmp = modelNamespace.model.split(".")
    func = tmp[-1]
    models = ".".join([i for i in tmp[:-1]])
    # 动态导入模块
    return importlib.import_module(models), func


# 反射
models, func = models()

func = getattr(models, func)

func()
