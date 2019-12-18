import requests

from master.call_worker.http_request import request_info
from master.logic.metadata import workers


def get_worker_info():
    res = []
    for worker in workers:
        cur_worker = {'url': worker}
        try:
            worker_info = request_info(worker, {})['data']
            cur_worker['info'] = worker_info
            cur_worker['status'] = 'OK'
        except requests.exceptions.ConnectionError:
            # worker is down!
            cur_worker['status'] = 'DOWN'

        res.append(cur_worker)

    return {'Success': True,
            'data': res}
