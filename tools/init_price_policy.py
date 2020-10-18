#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: init_price_policy.py
@time: 10/18/2020 9:38 PM
"""


from web import models


def run():
    exists = models.PricePolicy.objects.filter(
        category=1, title="个人免费版"
    ).exists()
    if not exists:
        models.PricePolicy.objects.create(
            category=1,
            title="个人免费版",
            price=0,
            project_num=3,
            project_member=2,
            project_space=20,
            per_file_size=5,
        )
    print("初始化价格策略成功")
