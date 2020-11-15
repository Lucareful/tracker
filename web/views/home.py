#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: home.py
@time: 10/15/2020 11:23 PM
"""
import json
import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from web import models
from django_redis import get_redis_connection


def index(request):
    return render(request, "index.html")
