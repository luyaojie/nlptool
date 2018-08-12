#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by Roger on 2018/8/12
import datetime
import os
import smtplib
import sys
import time
from email.mime.text import MIMEText

server_name = sys.argv[1]

CPU_SINGLE_TOP = 100
CPU_AVERAGE_TOP = 90
GPU_SINGLE_TOP = 100
GPU_AVERAGE_TOP = 90

pause = 180
mailto_list = ['experiment_logger@qq.com']
mail_host = "smtp.qq.com"
mail_user = "experiment_logger"  # 发送警报的邮箱
mail_pass = "hgjekugnxpnwdgji"  # 不是登录密码，是STMP密码
mail_postfix = "qq.com"


def send_email(to_list, sub, content):
    # Almost from https://blog.csdn.net/zcy0xy/article/details/79501170
    me = "GPU Auto Monitor" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except:
        print("send error!!!")
        return False


def get_max(numbers):
    return max(numbers) if numbers else 0.


def get_average(numbers):
    if numbers:
        return sum(numbers) / len(numbers)
    else:
        return 0.


def get_cpu_tem():
    shell_str = "sensors | awk '{print $3}' | grep '+'"
    result = os.popen(shell_str)
    temp_list = [float(temp[1:-3]) for temp in result.read().strip().split('\n')]
    return temp_list


def get_gpu_tem():
    shell_str = "nvidia-smi | awk '{print $3}' | grep 'C'"
    result = os.popen(shell_str)
    temp_list = [float(temp[:-1]) for temp in result.read().strip().split('\n')]
    return temp_list


send_email(mailto_list, "Start monitoring on %s" % server_name, "Start Monitoring")
while True:
    try:
        gpu_temp_list = get_gpu_tem()
        cpu_temp_list = get_cpu_tem()

        if get_max(gpu_temp_list) > GPU_SINGLE_TOP \
                or get_max(cpu_temp_list) > CPU_SINGLE_TOP \
                or get_average(gpu_temp_list) > GPU_AVERAGE_TOP \
                or get_average(cpu_temp_list) > CPU_AVERAGE_TOP:
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            warning_str = nowTime + '\n'
            warning_str += 'CPU Top Temp: %.2f\n' % get_max(cpu_temp_list)
            warning_str += 'CPU Ave Temp: %.2f\n' % get_average(cpu_temp_list)
            warning_str += 'GPU Top Temp: %.2f\n' % get_max(gpu_temp_list)
            warning_str += 'GPU Ave Temp: %.2f\n' % get_average(gpu_temp_list)
            print(warning_str)
            send_email(mailto_list, "%s Temp Warning!!!" % server_name, warning_str)
            print("send over")
    finally:
        time.sleep(pause)
