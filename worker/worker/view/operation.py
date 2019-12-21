# -*-coding:utf-8 -*-
from django.http import HttpResponse
import json


def handle_read(request):
    param = request.GET
    if 'name' not in param:
        res = {'success': False,
               'message': 'name parameter is not present in request'}
        return warp_to_response(res)

    return warp_to_response({})


def handle_write(request):
    param = request.GET
    if 'name' not in param:
        res = {'success': False,
               'message': 'name parameter is not present in request'}
        return warp_to_response(res)

    return warp_to_response({})


def warp_to_response(res):
    return HttpResponse(json.dumps(res, ensure_ascii=False))
