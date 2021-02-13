#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from web import models
from django_redis import get_redis_connection

from utils.encrypt import uid
from utils.alipay import AliPay


def index(request):
    return render(request, "index.html")


def price(request):
    """ 套餐 """
    # 获取套餐
    policy_list = models.PricePolicy.objects.filter(category=2)
    return render(request, "price.html", {"policy_list": policy_list})


def payment(request, policy_id):
    """ 支付页面"""
    # 1. 价格策略（套餐）policy_id
    policy_object = models.PricePolicy.objects.filter(
        id=policy_id, category=2
    ).first()
    if not policy_object:
        return redirect("price")

    # 2. 要购买的数量
    number = request.GET.get("number", "")
    if not number or not number.isdecimal():
        return redirect("price")
    number = int(number)
    if number < 1:
        return redirect("price")

    # 3. 计算原价
    origin_price = number * policy_object.price

    # 4.之前购买过套餐(之前掏钱买过）
    balance = 0
    _object = None
    if request.tracer.price_policy.category == 2:
        # 找到之前订单：总支付费用 、 开始~结束时间、剩余天数 = 抵扣的钱
        # 之前的实际支付价格
        _object = (
            models.Transaction.objects.filter(
                user=request.tracer.user, status=2
            )
            .order_by("-id")
            .first()
        )
        total_timedelta = _object.end_datetime - _object.start_datetime
        balance_timedelta = _object.end_datetime - datetime.datetime.now()
        if total_timedelta.days == balance_timedelta.days:
            # 按照价值进行计算抵扣金额
            balance = (
                _object.price_policy
                * price
                * _object.count
                / total_timedelta.days
                * (balance_timedelta.days - 1)
            )
        else:
            balance = (
                _object.price_policy
                * price
                * _object.count
                / total_timedelta.days
                * balance_timedelta.days
            )

    if balance >= origin_price:
        return redirect("price")

    context = {
        "policy_id": policy_object.id,
        "number": number,
        "origin_price": origin_price,
        "balance": round(balance, 2),
        "total_price": origin_price - round(balance, 2),
    }
    conn = get_redis_connection()
    key = "payment_{}".format(request.tracer.user.mobile_phone)
    # conn.set(key, json.dumps(context), nx=60 * 30)
    conn.set(
        key, json.dumps(context), ex=60 * 30
    )  # nx参数写错了，应该是ex（表示超时时间） ps：nx=True,表示redis中已存在key，再次执行时候就不会再设置了。

    context["policy_object"] = policy_object
    context["transaction"] = _object

    return render(request, "payment.html", context)


"""
def pay(request):

    conn = get_redis_connection()
    key = 'payment_{}'.format(request.tracer.user.mobile_phone)
    context_string = conn.get(key)
    if not context_string:
        return redirect('price')
    context = json.loads(context_string.decode('utf-8'))

    # 1. 数据库中生成交易记录（待支付）
    #     等支付成功之后，我们需要把订单的状态更新为已支付、开始&结束时间
    order_id = uid(request.tracer.user.mobile_phone)
    total_price = context['total_price']
    models.Transaction.objects.create(
        status=1,
        order=order_id,
        user=request.tracer.user,
        price_policy_id=context['policy_id'],
        count=context['number'],
        price=total_price
    )

    # 2. 跳转到支付去支付
    #    - 根据申请的支付的信息 + 支付宝的文档 => 跳转链接
    #    - 生成一个支付的链接
    #    - 跳转到这个链接
    # 构造字典
    params = {
        'app_id': "2016102400754054",
        'method': 'alipay.trade.page.pay',
        'format': 'JSON',
        'return_url': "http://127.0.0.1:8001/pay/notify/",
        'notify_url': "http://127.0.0.1:8001/pay/notify/",
        'charset': 'utf-8',
        'sign_type': 'RSA2',
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'version': '1.0',
        'biz_content': json.dumps({
            'out_trade_no': order_id,
            'product_code': 'FAST_INSTANT_TRADE_PAY',
            'total_amount': total_price,
            'subject': "tracer payment"
        }, separators=(',', ':'))
    }

    # 获取待签名的字符串
    unsigned_string = "&".join(["{0}={1}".format(k, params[k]) for k in sorted(params)])

    # 签名 SHA256WithRSA(对应sign_type为RSA2)
    from Crypto.PublicKey import RSA
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.Hash import SHA256
    from base64 import decodebytes, encodebytes

    # SHA256WithRSA + 应用私钥 对待签名的字符串 进行签名
    private_key = RSA.importKey(open("files/应用私钥2048.txt").read())
    signer = PKCS1_v1_5.new(private_key)
    signature = signer.sign(SHA256.new(unsigned_string.encode('utf-8')))

    # 对签名之后的执行进行base64 编码，转换为字符串
    sign_string = encodebytes(signature).decode("utf8").replace('\n', '')

    # 把生成的签名赋值给sign参数，拼接到请求参数中。

    from urllib.parse import quote_plus
    result = "&".join(["{0}={1}".format(k, quote_plus(params[k])) for k in sorted(params)])
    result = result + "&sign=" + quote_plus(sign_string)

    gateway = "https://openapi.alipaydev.com/gateway.do"
    ali_pay_url = "{}?{}".format(gateway, result)

    return redirect(ali_pay_url)
"""


def pay(request):
    conn = get_redis_connection()
    key = "payment_{}".format(request.tracer.user.mobile_phone)
    context_string = conn.get(key)
    if not context_string:
        return redirect("price")
    context = json.loads(context_string.decode("utf-8"))

    # 1. 数据库中生成交易记录（待支付）
    #     等支付成功之后，我们需要把订单的状态更新为已支付、开始&结束时间
    order_id = uid(request.tracer.user.mobile_phone)
    total_price = context["total_price"]
    models.Transaction.objects.create(
        status=1,
        order=order_id,
        user=request.tracer.user,
        price_policy_id=context["policy_id"],
        count=context["number"],
        price=total_price,
    )
    # 生成支付链接

    ali_pay = AliPay(
        appid=settings.ALI_APPID,
        app_notify_url=settings.ALI_NOTIFY_URL,
        return_url=settings.ALI_RETURN_URL,
        app_private_key_path=settings.ALI_PRI_KEY_PATH,
        alipay_public_key_path=settings.ALI_PUB_KEY_PATH,
    )
    query_params = ali_pay.direct_pay(
        subject="trace rpayment",  # 商品简单描述
        out_trade_no=order_id,  # 商户订单号
        total_amount=total_price,
    )
    pay_url = "{}?{}".format(settings.ALI_GATEWAY, query_params)
    return redirect(pay_url)


def pay_notify(request):
    """ 支付成功之后触发的URL """
    ali_pay = AliPay(
        appid=settings.ALI_APPID,
        app_notify_url=settings.ALI_NOTIFY_URL,
        return_url=settings.ALI_RETURN_URL,
        app_private_key_path=settings.ALI_PRI_KEY_PATH,
        alipay_public_key_path=settings.ALI_PUB_KEY_PATH,
    )

    if request.method == "GET":
        # 只做跳转，判断是否支付成功了，不做订单的状态更新。
        # 支付吧会讲订单号返回：获取订单ID，然后根据订单ID做状态更新 + 认证。
        # 支付宝公钥对支付给我返回的数据request.GET 进行检查，通过则表示这是支付宝返还的接口。
        params = request.GET.dict()
        sign = params.pop("sign", None)
        status = ali_pay.verify(params, sign)
        if status:
            """
            current_datetime = datetime.datetime.now()
            out_trade_no = params['out_trade_no']
            _object = models.Transaction.objects.filter(order=out_trade_no).first()

            _object.status = 2
            _object.start_datetime = current_datetime
            _object.end_datetime = current_datetime + datetime.timedelta(days=365 * _object.count)
            _object.save()
            """
            return HttpResponse("支付完成")
        return HttpResponse("支付失败")
    else:
        from urllib.parse import parse_qs

        body_str = request.body.decode("utf-8")
        post_data = parse_qs(body_str)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        sign = post_dict.pop("sign", None)
        status = ali_pay.verify(post_dict, sign)
        if status:
            current_datetime = datetime.datetime.now()
            out_trade_no = post_dict["out_trade_no"]
            _object = models.Transaction.objects.filter(
                order=out_trade_no
            ).first()

            _object.status = 2
            _object.start_datetime = current_datetime
            _object.end_datetime = current_datetime + datetime.timedelta(
                days=365 * _object.count
            )
            _object.save()
            return HttpResponse("success")

        return HttpResponse("error")
