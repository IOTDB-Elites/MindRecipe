from master.call_worker import http_request
from master.logic.metadata import article_category_map, workers, user_region_map


def get_popular():
    loc = check_popular()
    for i in loc:
        worker = workers[i]
        res = http_request.get_popular(worker)
        if bool(res['success']):
            return res

    return {'success': False,
            'message': 'Some error.',
            'data': {}}


def get_feedback(aid):
    loc = check_feedback()
    for i in loc:
        worker = workers[i]
        res = http_request.get_feedback(worker, {'aid': aid})
        if bool(res['success']) and len(res['data']) != 0:
            return res
    return {
        'success': False,
        'message': 'Unknown aid ' + aid,
        'data': {}
    }


def get_article(aid):
    for worker in workers:
        res = http_request.get_article(worker, {'aid': aid})
        if len(res['data']) != 0:
            return res

    return {'success': False,
            'message': 'Unknown aid: ' + aid,
            'data': {}}


# def get_article(aid, worker):
#     return http_request.get_article(worker, {'aid': aid})


def get_article_list(category, start, end):
    loc = check_category(category)
    if loc == -1:
        return {'success': False,
                'message': 'Unknown category: ' + category,
                'data': {}}
    for i in loc:
        worker = workers[i]
        res = http_request.get_article_list(worker, {'category': category, 'start': start, 'end': end})
        if bool(res['success']):
            return res

    return {'success': False,
            'message': 'No such category on sites' + str(loc),
            'data': {}}


# def update_user_info(user):
#     # check region is known
#     region = user['region']
#     loc = check_region(region)
#     if loc == -1:
#         return {'success': False,
#                 'message': 'Unknown user region: ' + region,
#                 'data': {}}
#
#     ## TODO consistency
#     # for worker in workers:
#     worker = workers[loc[0]]
#     res = http_request.update_user_info(worker, user)
#     return res

def check_region(region):
    return user_region_map.get(region, -1)


# def get_category_by_aid(aid):
#     for worker in workers:
#         res = http_request.get_article_list(worker, {'category': category, 'start': start, 'end': end})


def update_feedback(input_feedback):
    get_info = False
    loc_update_read = check_region(input_feedback['region'])
    loc_update_be_read = check_category(input_feedback['category'])

    for loc in loc_update_read:
        worker = workers[loc]
        res_read = http_request.update_read(worker, input_feedback)
        if bool(res_read['success']):
            get_info = True
            delta_comment = res_read['data']['delta_comment']
            delta_agree = res_read['data']['delta_agree']
            delta_share = res_read['data']['delta_share']
            delta_read = res_read['data']['delta_read']

    if not get_info:
        return {
            'success': False,
            'message': '(aid, uid) pair not found on any workers',
            'data': {}
        }

    print("here is the delta share, send to worker " + str(delta_share))
    input_feedback['delta_comment'] = delta_comment
    input_feedback['delta_agree'] = delta_agree
    input_feedback['delta_share'] = delta_share
    input_feedback['delta_read'] = delta_read

    for loc in loc_update_be_read:
        worker = workers[loc]
        res_read = http_request.update_be_read(worker, input_feedback)
        if not bool(res_read['success']):
            return {
                'success': False,
                'message': 'failed to update on worker: ' + worker,
                'data': {}
            }
    return {
        'success': True,
        'message': 'update success',
        'data': {}
    }



def check_category(category):
    return article_category_map.get(category, -1)


def check_popular():
    return [1]


def check_feedback():
    return [1]
