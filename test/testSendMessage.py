#!/usr/bin/env python
# encoding: utf-8
"""
@author: Luenci
@file: testSendMessage.py
@time: 9/12/2020 10:20 AM
"""
import random
from tarcker.settings import apiId, apiKey
from tarcker.settings import sign, smsAppId
from utils.tencent.sendSms import sendMessage


if __name__ == "__main__":
    res = sendMessage(apiId, apiKey, sign, smsAppId)
    code = random.randrange(10000, 99999)
    res.send_message(["+8618305299746"], "713710", ["21378"])
