# -*- coding: utf-8 -*-
# python 3.8.5
# @Time    : 2020-09-25
# @Author  : sibai

import random
import string


# 获取入参
def request_parse(req_data):
    '''
        解析请求数据并以json形式返回
    '''
    if req_data.method == 'POST' or req_data.method == 'DELETE':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


# 生成指定数量随机数
def random2Str(num):
    return ''.join(random.sample(string.ascii_letters + string.digits, num))


# 美化job
def beautify2Job(job):
    trigger = {}
    for t in job.trigger.fields:
        value = ''
        if not t.is_default:
            for e in t.expressions:
                value += str(e) + ','
            value = value[0:-1]
        else:
            value = '*'
        trigger[t.name] = value

    default = {
        'showDelete': False,
        'isLoop': True,
    }

    return {
        'id': job.id,
        'name': job.name,
        **job.args[0],
        **trigger,
        **default
    }


# 获取发送数据
def getSendMsg(data):
    return {
        'text': {
            "msgtype": "text",
            "text": {
                "content": data.get('content')
            },
            "at": {
                "atMobiles": data.get('atMobiles').split(','),
                "isAtAll": data.get('isAtAll')
            }
        },
        'link': {},
        'markdown': {},
        'singleActionCard': {},
        'ActionCard': {},
        'feedCard': {},
    }.get(data.get('model'), {})
