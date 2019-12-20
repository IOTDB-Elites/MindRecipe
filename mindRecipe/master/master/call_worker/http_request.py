import requests

HEARTBEAT_API = '/api/admin/heartbeat'
REPORT_API = '/api/admin/report'
HTTP = 'http://'


def request_heartbeat(url):
    response = requests.get(HTTP + url + HEARTBEAT_API)
    return response.json()


def request_info(url, data):
    response = requests.get(HTTP + url + REPORT_API, data=data)
    return response.json()
