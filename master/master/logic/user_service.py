from master.call_worker import http_request
from master.logic.metadata import user_region_map, workers


def get_user_info(name, region):
    # check region is known
    loc = check_region(region)
    if loc == -1:
        return {'success': False,
                'message': 'Unknown user region: ' + region,
                'data': {}}

    for i in loc:
        worker = workers[i]
        res = http_request.get_user_info(worker, {'name': name, 'region': region})
        if bool(res['success']):
            return res
    return {'success': False,
            'message': 'Unknown user on any region.',
            'data': {}}


def get_read_list(uid, region):
    loc = check_region(region)
    if loc == -1:
        return {'success': False,
                'message': 'Unknown user region: ' + region,
                'data': {}}
    for i in loc:
        worker = workers[i]
        res = http_request.get_read_list(worker, {'uid': uid})
        if bool(res['success']):
            return res

    return {'success': False,
            'message': 'Unknown user on any sites.',
            'data': {}}


def update_user_info(user):
    # check region is known
    region = user['region']
    loc = check_region(region)
    if loc == -1:
        return {'success': False,
                'message': 'Unknown user region: ' + region,
                'data': {}}

    ## TODO consistency
    # for worker in workers:
    worker = workers[loc[0]]
    res = http_request.update_user_info(worker, user)
    return res


def check_region(region):
    return user_region_map.get(region, -1)
