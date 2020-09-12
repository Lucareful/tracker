#!/usr/bin/env python
# encoding: utf-8
'''
@author: Luenci
@file: sendSms.py
@time: 9/7/2020 10:39 PM
'''
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20190711 import models
from tencentcloud.sms.v20190711 import sms_client

from tarcker.settings import secretId
from tarcker.settings import secretKey
from tarcker.settings import sign
# 导入 SMS 模块的client models


class requestSms(models.SendSmsRequest):
    """
    重写SendSmsRequest类的构造方法，使其可以接收字典一次实例化
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)


class sendMessage(object):
    """
    实例化secretId 和 secretKey sign
    """

    def __init__(self, secretId, secretKey, sign):
        self.secretId = secretId
        self.secretKey = secretKey
        self.sign = sign

    def send_message(self, PhoneNumberSet, TemplateID, TemplateParamSet):
        """
        :param PhoneNumberSet: 发送手机号
        :param TemplateID: 短信模板ID
        :param TemplateParamSet: 模板中的参数
        :return:
        """
        cred = credential.Credential(self.secretId, self.secretKey)

        # 实例化 SMS 的 client 对象
        # 第二个参数是地域信息，可以直接填写字符串 ap-guangzhou，或者引用预设的常量
        client = sms_client.SmsClient(cred, region='ap-guangzhou')

        messageDict = {
            'PhoneNumberSet': PhoneNumberSet,
            'TemplateID': TemplateID,
            'SmsSdkAppid': int(secretId),
            'Sign': sign,
            'TemplateParamSet': TemplateParamSet,

        }

        # 实例化一个请求对象，根据调用的接口和实际情况，可以进一步设置请求参数
        req = requestSms(**messageDict)

        try:
            # 通过 client 对象调用 SendSms 方法发起请求。注意请求方法名与请求对象是对应的
            resp = client.SendSms(req)
            # 输出 JSON 格式的字符串回包
            print(resp.to_json_string(indent=1))
        except TencentCloudSDKException as err:
            print(err)
        return None


# from qcloudsms_py import SmsMultiSender, SmsSingleSender
# from qcloudsms_py.httpclient import HTTPError
# from tarcker.settings import (secretId, sign, secretKey)
#
#
# class sendMessage(object):
#     def __init__(self):
#         self.secretId = secretId
#         self.secretKey = secretKey
#         self.sign = sign
#
#     def send_sms_single(self, phone_num, template_id, template_param_list):
#         """
#         单条发送短信
#         :param phone_num: 手机号
#         :param template_id: 腾讯云短信模板ID
#         :param template_param_list: 短信模板所需参数列表，例如:【验证码：{0}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
#         :return:
#         """
#         appid = self.secretId  # 自己应用ID
#         appkey = self.secretKey  # 自己应用Key
#         sms_sign = self.sign  # 自己腾讯云创建签名时填写的签名内容（使用公众号的话这个值一般是公众号全称或简称）
#         sender = SmsSingleSender(appid, appkey)
#         try:
#             response = sender.send_with_param(86, phone_num, template_id, template_param_list, sign=sms_sign)
#         except HTTPError as e:
#             response = {'result': e, 'errmsg': "网络异常发送失败"}
#         return response
#
#     def send_sms_multi(self, phone_num_list, template_id, param_list):
#         """
#         批量发送短信
#         :param phone_num_list:手机号列表
#         :param template_id:腾讯云短信模板ID
#         :param param_list:短信模板所需参数列表，例如:【验证码：{0}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
#         :return:
#         """
#         appid = self.secretId
#         appkey = self.secretKey
#         sms_sign = self.sign
#         sender = SmsMultiSender(appid, appkey)
#         try:
#             response = sender.send_with_param(85, phone_num_list, template_id, param_list, sign=sms_sign)
#         except HTTPError as e:
#             response = {'result': e, 'errmsg': "网络异常发送失败"}
#         return response
if __name__ == '__main__':
    res = sendMessage(secretId, secretKey, sign)
    import random

    code = random.randrange(1000, 9999)
    res.send_message(['+8617371246916'], '713710', [code, ])
