import requests

REQUEST_API = '/api/admin/heartbeat'
HTTP = 'http://'


def request_heartbeat(url, data):
    response = requests.get(HTTP + url + REQUEST_API, data=data)
    return response.json()


def request_info(url, data):
    response = requests.get(HTTP + url + REQUEST_API, data=data)
    return response.json()
