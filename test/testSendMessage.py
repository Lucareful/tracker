#!/usr/bin/env python
# encoding: utf-8
'''
@author: Luenci
@file: testSendMessage.py
@time: 9/12/2020 10:20 AM
'''
import random

from utils.tencent.sendSms import sendMessage

# 实例化短信对象
sms = sendMessage()
# 发送单条短信
code = random.randrange(10000, 99999)
res = sms.send_sms_single('17371246916', 713710, [code, ])
print(res)
