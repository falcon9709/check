#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

import requests

# 填入glados账号对应cookie
GLADOS_COOKIE = os.environ["GLADOS_COOKIE"]
cookies = GLADOS_COOKIE.split('\n')
PUSHPLUS_TOKEN = os.environ["PUSHPLUS_TOKEN"]

session = requests.session()


# push推送
def pushplus_bot(title, content):
    try:
        if not PUSHPLUS_TOKEN:
            print("PUSHPLUS服务的token未设置!!\n取消推送")
            return
        print("PUSHPLUS服务启动")
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": PUSHPLUS_TOKEN,
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=body, headers=headers).json()
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)


def checkin(cookie):
    checkin_url = "https://glados.rocks/api/user/checkin"
    state_url = "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    payload = {"token": "glados.one"}
    head1 = {
        'cookie': cookie,
        'referer': referer,
        'origin': origin,
        'user-agent': useragent,
        'content-type': 'application/json;charset=UTF-8'
    }
    head2 = {
        'cookie': cookie,
        'referer': referer,
        'origin': origin,
        'user-agent': useragent
    }
    try:
        checkin = session.post(checkin_url, headers=head1, data=json.dumps(payload))
        state = session.get(state_url, headers=head2)
    except Exception as e:
        print(f"签到失败，请检查网络：{e}")
        return None, None, None
    try:
        mess = checkin.json()['message']
        mail = state.json()['data']['email']
        time = state.json()['data']['leftDays'].split('.')[0]
    except Exception as e:
        print(f"解析登录结果失败：{e}")
        return None, None, None
    return mess, time, mail


def main():
    title = "GlaDOS签到通知"
    contents = []
    if not cookies:
        return ""
    for cookie in cookies:
        ret, remain, email = checkin(cookie)
        content = f"账号：{email}\n签到结果：{ret}\n剩余天数：{remain}\n"
        print(f"账号：{str(email[0:2])}****{str(email[-4:-1])}\n签到结果：{ret}\n剩余天数：{remain}\n")
        contents.append(content)
    contents_str = "".join(contents)
    pushplus_bot(title, contents_str)


def main_handler(event, context):
    return main()


if __name__ == '__main__':
    main()
