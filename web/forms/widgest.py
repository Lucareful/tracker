#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: widgest.py
@time: 11/8/2020 12:56 PM
"""

from django.forms import RadioSelect


class ColorRadioSelect(RadioSelect):
    """
    自定义form RadioSelect插件样式
    """

    template_name = "widgets/color_radio/radio.html"
    option_template_name = "widgets/color_radio/radio_option.html"
