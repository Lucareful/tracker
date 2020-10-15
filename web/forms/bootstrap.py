#!/usr/bin/env python
# encoding: utf-8
'''
@author: Luenci
@file: bootstrap.py
@time: 10/15/2020 10:39 PM
'''

from typing import List


class BootStrapForm(object):
    bootstrap_class_exclude: List = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.bootstrap_class_exclude:
                continue
            old_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = '{} form-control'.format(old_class)
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)
