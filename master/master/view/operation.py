# -*-coding:utf-8 -*-
import json

from django.http import HttpResponse

from master.logic import user_service, article_service, worker_op

GET_USER_INFO_PARAMS = ['name', 'region']
UPDATE_USER_INFO_PARAMS = ['region']

UPDATE_USER_INFO_PARAMS = ['region', 'dept', 'language', 'role', 'gender',
                           'name', 'uid', 'phone', 'timestamp', 'email',
                           'preferTags', 'grade', 'obtainedCredits']
UPDATE_FEEDBACK_PARAMS = ['uid', 'aid', 'readTimeLength', 'readSequence', 'readOrNot', 'agreeOrNot', 'commentOrNot',
                          'commentDetail', 'shareOrNot']

ADD_DBMS_PARAM = ['ip', 'db_port']
REMOVE_DBMS_PARAM = ['ip']

GET_ARTICLE_LIST = ['category']
GET_ARTICLE = ['aid']
GET_FEEDBACK = ['aid']
GET_READ_LIST = ['uid']


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
    return warp_to_response(
        user_service.get_user_info(param['name'], param['region']))


def get_read_list(request):
    error_res = check_get_param(request, GET_READ_LIST)
    if error_res is not None:
        return warp_to_response(error_res)

    param = request.GET
    return warp_to_response(
        user_service.get_read_list(param['uid'], param['region']))


def get_article_list(request):
    error_res = check_get_param(request, GET_ARTICLE_LIST)
    if error_res is not None:
        return warp_to_response(error_res)
    param = request.GET
    return warp_to_response(
        article_service.get_article_list(param['category'], param['start'], param['end']))


def add_dbms(request):
    error_res = check_get_param(request, ADD_DBMS_PARAM)
    if error_res is not None:
        return warp_to_response(error_res)
    param = request.GET
    return warp_to_response(worker_op.add_worker(param['ip'], param['db_port']))

def remove_dbms(request):
    error_res = check_get_param(request, REMOVE_DBMS_PARAM)
    if error_res is not None:
        return warp_to_response(error_res)
    param = request.GET
    return warp_to_response(worker_op.remove_worker(param['ip']))
    return None

def get_popular(request):
    return warp_to_response(article_service.get_popular())


def get_feedback(request):
    error_res = check_get_param(request, GET_FEEDBACK)
    if error_res is not None:
        return warp_to_response(error_res)
    param = request.GET
    return warp_to_response(article_service.get_feedback(param['aid']))


def get_article(request):
    error_res = check_get_param(request, GET_ARTICLE)
    if error_res is not None:
        return warp_to_response(error_res)
    param = request.GET
    return warp_to_response(
        article_service.get_article(param['aid'])
    )


# post method
def update_user_info(request):
    # check params
    user = post_request_to_json(request.body)
    error_res = check_post_param(user, UPDATE_USER_INFO_PARAMS)
    if error_res is not None:
        return warp_to_response(error_res)

    return warp_to_response(
        user_service.update_user_info(user))


def feedback(request):
    input_feedback = post_request_to_json(request.body)
    error_res = check_post_param(input_feedback, UPDATE_FEEDBACK_PARAMS)
    if error_res is not None:
        return warp_to_response(error_res)
    return warp_to_response(
        article_service.update_feedback(input_feedback)
    )


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


