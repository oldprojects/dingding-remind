# -*- coding: utf-8 -*-
# python 3.8.5
# @Time    : 2020-09-21
# @Author  : sibai


from flask import Flask, render_template, request
import common.printMsg
import common.utils
import dingding.dingding_robot
from flask_apscheduler import APScheduler
import json
import time


# 解决flask与vue共同使用花括号的冲突
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


# app = Flask(__name__)
app = CustomFlask(__name__)
# 破蛋日(单位: ms)
birthday_time = time.mktime(time.strptime('2020-09-25 00:00:00', '%Y-%m-%d %H:%M:%S')) * 1000
# 手动维护定时器状态
scheduler_status = 'shutdown'

'''
    ==========以下为定时器自身api==========
'''


# 启动
@app.route('/start', methods=['GET'])
def start():
    global scheduler_status
    scheduler.start()
    scheduler_status = 'start'
    return '启动成功...'


# 暂停
@app.route('/pause', methods=['GET'])
def pause():
    global scheduler_status
    scheduler.pause()
    scheduler_status = 'pause'
    return '暂停成功...'


# 恢复
@app.route('/resume', methods=['GET'])
def resume():
    global scheduler_status
    scheduler.resume()
    scheduler_status = 'resume'
    return '恢复成功...'


# 停止
@app.route('/shutdown', methods=['GET'])
def shutdown():
    global scheduler_status
    scheduler.shutdown()
    scheduler_status = 'shutdown'
    return '停止成功...'


# 获取状态
@app.route('/status', methods=['GET'])
def status():
    return scheduler_status


'''
    ==========以下为操作具体定时任务api==========
'''


# 获取列表详情
@app.route('/remind/getList', methods=['GET'])
def remind_getList():
    respList = []
    jobs = scheduler.get_jobs()
    for job in jobs:
        respList.append(common.utils.beautify2Job(job))
    return json.dumps(respList)


# 获取单个详情
@app.route('/remind/getById', methods=['GET'])
def remind_getById():
    params = common.utils.request_parse(request)
    job = scheduler.get_job(params.get('id'))
    return json.dumps(common.utils.beautify2Job(job))


# 添加job
@app.route('/remind/add', methods=['POST'])
def remind_add():
    data = common.utils.request_parse(request)
    id = 'job_' + common.utils.random2Str(7)
    sendMsg = common.utils.getSendMsg(data)

    # 周
    day_of_week = '*'
    if data.get('week').__len__() > 0:
        day_of_week = ','.join(data.get('week'))

    # 时
    hour = '*'
    if data.get('hour').__len__() > 0:
        hour = ','.join(str(i) for i in data.get('hour'))

    # 分
    minute = '*'
    if data.get('minute').__len__() > 0:
        minute = ','.join(str(i) for i in data.get('minute'))

    # 秒
    second = '*'
    if data.get('second').__len__() > 0:
        second = ','.join(str(i) for i in data.get('second'))

    scheduler.add_job(id=id,
                      name=data.get('name'),
                      func=dingding.dingding_robot.sendMsg2DingDing,
                      args=[sendMsg],
                      trigger='cron',
                      day_of_week=day_of_week,
                      hour=hour,
                      minute=minute,
                      second=second
                      )
    return '[%s]添加成功...' % data.get('name')


# 修改job
@app.route('/remind/modify', methods=['POST'])
def remind_modify():
    data = common.utils.request_parse(request)
    sendMsg = common.utils.getSendMsg(data)

    scheduler.modify_job(id=data.get('id'),
                         func=dingding.dingding_robot.sendMsg2DingDing,
                         args=[sendMsg]
                         )
    return '[%s]修改成功...' % data.get('name')


# 删除job
@app.route('/remind/deleteById', methods=['DELETE'])
def remind_deleteById():
    data = common.utils.request_parse(request)
    scheduler.remove_job(data.get('id'))
    return '删除成功...'


'''
    ==========以下为公共api==========
'''


# 首页
@app.route('/')
def hello_world():
    return render_template('index.html', title='首页')


# 获取破蛋日
@app.route('/getBirthday')
def birthday():
    return str(int(birthday_time))


# 程序主入口
if __name__ == '__main__':
    common.printMsg.copyRight()
    # 注入 apscheduler
    scheduler = APScheduler()
    scheduler.init_app(app)

    app.run(host='0.0.0.0', port=9090, debug=False)
