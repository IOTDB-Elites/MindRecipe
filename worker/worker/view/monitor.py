# -*-coding:utf-8 -*-
from django.http import HttpResponse
import json

from worker.logic.monitor import report


def receive_heartbeat(request):
    return warp_to_response({'Success': True})


def receive_report(request):
    return warp_to_response(report())


def warp_to_response(res):
    return HttpResponse(json.dumps(res, ensure_ascii=False))
