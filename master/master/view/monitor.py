# -*-coding:utf-8 -*-
from django.http import HttpResponse
import json

from master.logic.monitor import get_worker_info


def monitor(request):
    return warp_to_response(get_worker_info())


def warp_to_response(res):
    return HttpResponse(json.dumps(res, ensure_ascii=False))
