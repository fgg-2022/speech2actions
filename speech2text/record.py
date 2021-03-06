#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date    : 2018-12-02 19:04:55
import wave
import requests
import time
import base64
from pyaudio import PyAudio, paInt16
import webbrowser

framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILENAME = '../audio/speech'

base_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
APIKey = "C84a1AHter2NInG6iF2g6sCQ" # 在个人页面复制
SecretKey = "u0XkO6mNtHORgDQl1S5AVjjIkYqEpEDI"

HOST = base_url % (APIKey, SecretKey)


def getToken(host):
    res = requests.post(host)
    return res.json()['access_token']


def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()


def get_audio(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data


def speech2text(speech_data, token, dev_pid=1537):
    FORMAT = 'wav'
    RATE = '16000'
    CHANNEL = 1
    CUID = '*******'
    SPEECH = base64.b64encode(speech_data).decode('utf-8')

    data = {
        'format': FORMAT,
        'rate': RATE,
        'channel': CHANNEL,
        'cuid': CUID,
        'len': len(speech_data),
        'speech': SPEECH,
        'token': token,
        'dev_pid': dev_pid
    }
    url = 'https://vop.baidu.com/server_api'
    headers = {'Content-Type': 'application/json'}
    # r=requests.post(url,data=json.dumps(data),headers=headers)
    print('正在识别...')
    r = requests.post(url, json=data, headers=headers)
    Result = r.json()
    if 'result' in Result:
        return Result['result'][0]
    else:
        return Result


def do_transfer(file_path):
    print('================================ BEGIN: Get sentence from record file ================================')
    TOKEN = getToken(HOST)
    speech = get_audio(file_path)
    result = speech2text(speech, TOKEN, 1737)
    print('================================ Done: Get sentence from record file ================================')

    return result


if __name__ == '__main__':
    flag = 'y'
    r = 1
    while r < 6:
        do_transfer(FILENAME + str(r) + '.wav')
        r = r + 1

# i want a square on a table