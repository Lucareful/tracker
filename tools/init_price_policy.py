#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: init_price_policy.py
@time: 10/18/2020 9:38 PM
"""
import uuid

import arrow

from web import models
from utils import encrypt


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


def test():
    password = encrypt.md5("123")
    user = models.UserInfo.objects.create(
        username="test",
        password=password,
        mail="test@123.com",
        mobilePhone="17371246916",
    )
    policy_obj = models.PricePolicy.objects.filter(
        category=1, title="个人免费版"
    ).first()
    models.Transaction.objects.create(
        status=2,
        order=str(uuid.uuid4()),
        user=user,
        price_policy=policy_obj,
        count=0,
        price=0,
        start_datetime=arrow.now().format(),
    )
    print("初始化测试用户成功")
