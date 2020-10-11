#!/usr/bin/env python
# encoding: utf-8
'''
@author: Luenci
@file: sendSms.py
@time: 9/7/2020 10:39 PM
'''
import json

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.sms.v20190711 import models
from tencentcloud.sms.v20190711 import sms_client

from tarcker.settings import apiId, apiKey
from tarcker.settings import sign, smsAppId
# 导入 SMS 模块的client models


class requestSms(models.SendSmsRequest):
    """
    重写SendSmsRequest类的构造方法，使其可以接收字典一次实例化
    """

    def __init__(self, requestDic):
        super().__init__()
        self.__dict__.update(requestDic)


class sendMessage(object):
    """
    实例化secretId 和 secretKey sign
    """

    def __init__(self, apiId, apiKey, sign, smsAppId):
        self.apiId = apiId
        self.apiKey = apiKey
        self.smsAppId = smsAppId
        self.sign = sign

    def send_message(self, PhoneNumberSet, TemplateID, TemplateParamSet):
        """
        :param PhoneNumberSet: 发送手机号
        :param TemplateID: 短信模板ID
        :param TemplateParamSet: 模板中的参数
        :return:
        """
        cred = credential.Credential(self.apiId, self.apiKey)

        # 实例化一个 http 选项，可选，无特殊需求时可以跳过
        httpProfile = HttpProfile()
        httpProfile.reqMethod = 'POST'  # POST 请求（默认为 POST 请求）
        httpProfile.reqTimeout = 30  # 请求超时时间，单位为秒（默认60秒）
        # httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名（默认就近接入）

        # 非必要步骤:
        # 实例化一个客户端配置对象，可以指定超时时间等配置
        clientProfile = ClientProfile()
        clientProfile.signMethod = 'TC3-HMAC-SHA256'  # 指定签名算法
        clientProfile.language = 'en-US'
        clientProfile.httpProfile = httpProfile
        # 实例化 SMS 的 client 对象
        # 第二个参数是地域信息，可以直接填写字符串 ap-guangzhou，或者引用预设的常量
        client = sms_client.SmsClient(cred, 'ap-shanghai', clientProfile)

        messageDict = {
            'PhoneNumberSet': PhoneNumberSet,
            'TemplateID': TemplateID,
            'SmsSdkAppid': smsAppId,
            'Sign': sign,
            'TemplateParamSet': TemplateParamSet,

        }

        # 实例化一个请求对象，根据调用的接口和实际情况，可以进一步设置请求参数
        req = requestSms(messageDict)

        try:
            # 通过 client 对象调用 SendSms 方法发起请求。注意请求方法名与请求对象是对应的
            resp = client.SendSms(req)
            # 输出 JSON 格式的字符串回包
            print(resp.to_json_string(indent=2))
            resp = json.loads(resp.to_json_string(indent=0).replace(r'\n', '')).get('SendStatusSet')[0]
            return resp
        except TencentCloudSDKException as err:
            print(err)
            err = {key.capitalize(): value for key, value in err.__dict__.items()}
            return err


# if __name__ == '__main__':
#     res = sendMessage(apiId, apiKey, sign, smsAppId)
#     import random
#
#     code = random.randrange(10000, 99999)
#     res.send_message(['+8618305299746'], '713710', ['21378'])
