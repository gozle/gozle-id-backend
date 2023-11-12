#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import time
import uuid
import requests

API_URL = 'http://172.16.1.213:7001/api/'
USER = 'gozle'
SECRET = b'P7t+1fw0VzRZllYhsP5mFMsu1iOff7YACdc3LLW4IQA='
#DEST = '99361960135'
#TEXT = 'test'


def get_cleaned_phone_number(number):
    return number[1:] if number[0] == '+' else number


def generate_hmac(key, message):
    key = base64.b64decode(key)
    msg = message.encode('utf-8')
    h = hmac.new(key, msg, hashlib.sha256).digest()
    return base64.b64encode(h)


def send_message(user, msg_id, dest, text, secret):
    ts = int(time.time())
    msg = '%s:%s:%s:%s:%s' % (user, msg_id, dest, text, ts)
    print(msg)
    req_hmac = generate_hmac(secret, msg)
    return requests.post(API_URL + user + '/send', data={
        'msg-id': msg_id,
        'dest': dest,
        'text': text,
        'ts': ts,
        'hmac': req_hmac
    })


def check_sms_status(user, msg_ids, secret):
    ts = int(time.time())
    s_msg_ids = ','.join(msg_ids)
    msg = '%s:%s:%s' % (user, s_msg_ids, ts)
    req_hmac = generate_hmac(secret, msg)
    return requests.post(API_URL + user + '/status', data={
        'msg-ids': s_msg_ids,
        'ts': ts,
        'hmac': req_hmac
    })


def send(dest, text):
    dest = get_cleaned_phone_number(dest)
    msg_id = uuid.uuid4()
    rv = send_message(user=USER, msg_id=uuid.uuid4(), dest=dest, text=text, secret=SECRET)
#    rv = check_sms_status(USER, ['77af938b-915a-40eb-bb57-40d3a26776cb'], SECRET)
    print(rv.status_code, rv.content)


#import threading
#if __name__ == '__main__':
#    for i in range(15):
#        threading.Thread(target=send).start()
