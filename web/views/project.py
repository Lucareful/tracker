#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: project.py
@time: 10/24/2020 11:26 AM
"""

from django.http import HttpResponse
from django.shortcuts import render


def project_list(request):

    return render(request, "project_list.html")
