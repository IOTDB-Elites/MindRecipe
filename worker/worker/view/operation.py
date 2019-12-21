# -*-coding:utf-8 -*-
from django.http import HttpResponse
import json

from worker.logic import user_service
from worker.logic import article_service

GET_USER_INFO_PARAMS = ['name']
UPDATE_USER_INFO_PARAMS = ['uid']
GET_ARTICLE_LIST = ['category']


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


# get method
def get_user_info(request):
    # check params
    error_res = check_get_param(request, GET_USER_INFO_PARAMS)
    if error_res is not None:
        return warp_to_response(error_res)

    param = request.GET
    print(param)
    return warp_to_response(
        user_service.get_user_info(param['name'], param['region']))


def get_article_list(request):
    error_res = check_get_param(request, GET_ARTICLE_LIST)
    if error_res is not None:
        return warp_to_response(error_res)
    param = request.GET
    print(param)
    return warp_to_response(
        article_service.get_article_list(param['category']))


# post method
def update_user_info(request):
    # check params
    user = post_request_to_json(request.body)
    error_res = check_post_param(user, UPDATE_USER_INFO_PARAMS)
    if error_res is not None:
        return warp_to_response(error_res)

    return warp_to_response(
        user_service.update_user_info(user))


def warp_to_response(res):
    return HttpResponse(json.dumps(res, ensure_ascii=False))


def check_get_param(request, params):
    for param in params:
        if param not in request.GET:
            return {'success': False,
                    'message': param + ' parameter is not present in request'}

    return None


def check_post_param(data, params):
    for param in params:
        if param not in data:
            return {'success': False,
                    'message': param + ' parameter is not present in request'}

    return None


def post_request_to_json(body):
    return json.loads(body.decode('utf-8'))
