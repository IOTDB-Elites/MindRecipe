from master.call_worker import http_request
from master.logic.metadata import user_region_map, article_category_map, workers


def get_user_info(name, region):
    # check region is known
    loc = check_region(region)
    if loc == -1:
        return {'Success': True,
                'message': 'Unknown user region: ' + region,
                'data': {}}

    worker = workers[loc]
    return http_request.get_user_info(worker, {'name': name})


def update_user_info(region, user):
    # check region is known
    loc = check_region(region)
    if loc == -1:
        return {'Success': True,
                'message': 'Unknown user region: ' + region,
                'data': {}}

    worker = workers[loc]
    return http_request.update_user_info(worker, user)


def check_region(region):
    return user_region_map.get(region, -1)


def check_category(category):
    return article_category_map.get(category, -1)
