from master.call_worker import http_request
from master.logic.metadata import article_category_map, workers


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
        print(res)
        if len(res['data']) != 0:
            return res

    return {'success': False,
            'message': 'Unkown aid: ' + aid,
            'data': {}}


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


def check_category(category):
    return article_category_map.get(category, -1)


def check_popular():
    return [1]


def check_feedback():
    return [1]
