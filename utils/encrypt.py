#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: encrypt.py
@time: 10/11/2020 9:44 PM
"""
import hashlib
import uuid

from django.conf import settings


def md5(password):
    """MD5加密"""
    hash_object = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    hash_object.update(password.encode("utf-8"))
    return hash_object.hexdigest()


def uid(string):
    data = "{}-{}".format(str(uuid.uuid4()), string)
    return md5(data)
