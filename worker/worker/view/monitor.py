# -*-coding:utf-8 -*-
from django.http import HttpResponse
import json


def receive_heartbeat(request):
    res = {'success': True,
           'message': 'Receive heart beat',
           'data': {}}
    return warp_to_response(res)


def warp_to_response(res):
    return HttpResponse(json.dumps(res, ensure_ascii=False))
