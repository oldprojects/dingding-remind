# -*- coding: utf-8 -*-
# python 3.8.5
# @Time    : 2020-09-25
# @Author  : sibai


import time
import hmac
import hashlib
import base64
from urllib import parse
import requests
import json

# 钉钉机器人主地址
webhook = 'https://oapi.dingtalk.com/robot/send?'
# 钉钉机器人token
token = '77f73c338361040c7c8da921710859740dfadeccc2009f7445116bcdca540450'
# 钉钉机器人密钥
secret = 'SECf6d63d0254507d9ff508d301eaa92e5adaaa25d641e7b19be9f6d6092c59e46d'


# 发送消息到群
def sendMsg2DingDing(sendData):
    print('开始发送消息到钉钉群...')
    signature = calculateSignature(secret)
    signature['access_token'] = token
    params = parse.urlencode(signature)

    url = webhook + params
    data = json.dumps(sendData)

    headers = {
        'Accept-Charset': 'utf-8',
        'Content-Type': 'application/json'
    }
    print('发送数据: ', sendData)
    resp = requests.post(url=url, data=data, headers=headers)
    print('返回结果: ', resp.json())


# 官方签名生成算法
def calculateSignature(secretKey):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secretKey.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secretKey)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = parse.quote_plus(base64.b64encode(hmac_code))
    return {
        'timestamp': timestamp,
        'sign': sign
    }
