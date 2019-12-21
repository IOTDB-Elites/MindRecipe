import json

import requests

HEARTBEAT_API = '/api/admin/heartbeat'
REPORT_API = '/api/admin/report'
GET_USER_INFO_API = '/api/user/get_info'
UPDATE_USER_INFO_API = '/api/user/update_info'

HTTP = 'http://'

RETRY_COUNT = 2


def request_heartbeat(url):
    return send_get_request(HTTP + url + HEARTBEAT_API, {})


def request_info(url, data):
    return send_get_request(HTTP + url + REPORT_API, data)


def get_user_info(url, data):
    return send_get_request(HTTP + url + GET_USER_INFO_API, data)


def update_user_info(url, data):
    return send_post_request(HTTP + url + UPDATE_USER_INFO_API, data)


def send_get_request(url, data):
    for i in range(RETRY_COUNT):
        try:
            response = requests.get(url, params=data)
            return response.json()
        except:
            print('retry count: ', i + 1)

    return {'success': False,
            'message': 'worker unreachable, please retry'}


def send_post_request(url, data):
    for i in range(RETRY_COUNT):
        try:
            print(data)
            print(json.dumps(data))
            response = requests.post(url, data=json.dumps(data))
            return response.json()
        except:
            print('retry count: ', i + 1)

    return {'success': False,
            'message': 'worker unreachable, please retry'}
