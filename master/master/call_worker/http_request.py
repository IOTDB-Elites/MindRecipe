import json

import requests

HEARTBEAT_API = '/api/admin/heartbeat'
REPORT_API = '/api/admin/report'
GET_USER_INFO_API = '/api/user/get_info'
UPDATE_USER_INFO_API = '/api/user/update_info'
GET_READ_LIST = '/api/user/get_read_list'
GET_ARTICLE_LIST = '/api/article/get_list'
GET_POPULAR = '/api/article/get_popular'
GET_ARTICLE = '/api/article/get_article'
GET_FEEDBACK = '/api/article/get_feedback'
UPDATE_FEEDBACK = '/api/article/feedback'
UPDATE_READ = '/api/read/update_read'
UPDATE_BE_READ = '/api/read/update_be_read'
REMOVE_DBMS = 'api/admin/shut_down'

HTTP = 'http://'

RETRY_COUNT = 2


def request_heartbeat(url):
    return send_get_request(HTTP + url + HEARTBEAT_API, {}, 2)


def request_info(url, data):
    return send_get_request(HTTP + url + REPORT_API, data)


def get_user_info(url, data):
    return send_get_request(HTTP + url + GET_USER_INFO_API, data)


def get_read_list(url, data):
    return send_get_request(HTTP + url + GET_READ_LIST, data)


def get_article_list(url, data):
    return send_get_request(HTTP + url + GET_ARTICLE_LIST, data)


def update_user_info(url, data):
    return send_post_request(HTTP + url + UPDATE_USER_INFO_API, data)


def update_feedback(url, data):
    return send_post_request(HTTP + url + UPDATE_FEEDBACK, data)


def update_read(url, data):
    return send_post_request(HTTP + url + UPDATE_READ, data)


def update_be_read(url, data):
    return send_post_request(HTTP + url + UPDATE_BE_READ, data)


def get_popular(url):
    return send_get_request(HTTP + url + GET_POPULAR, {})


def get_article(url, data):
    return send_get_request(HTTP + url + GET_ARTICLE, data)


def get_feedback(url, data):
    return send_get_request(HTTP + url + GET_FEEDBACK, data)


def remove_dbms(url, data):
    send_get_request(HTTP + url + REMOVE_DBMS, data)


def send_get_request(url, data, time_out=None):
    for i in range(RETRY_COUNT):
        try:
            response = requests.get(url, params=data, timeout=time_out)
            return response.json()
        except:
            print('retry count: ', i + 1)

    print("here")
    return {'success': False,
            'message': 'worker unreachable, please retry'}


def send_post_request(url, data):
    for i in range(RETRY_COUNT):
        try:
            response = requests.post(url, data=json.dumps(data))
            return response.json()
        except:
            print('retry count: ', i + 1)

    return {'success': False,
            'message': 'worker unreachable, please retry'}
