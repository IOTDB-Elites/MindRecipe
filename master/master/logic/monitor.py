import requests

from master.call_worker.http_request import request_info
from master.logic.metadata import workers


def get_worker_info():
    res = []
    for i in range(len(workers)):
        loc = i % 2
        worker = workers[loc]
        cur_worker = {'url': workers[i]}
        if worker.split(":")[1] == '8001':
            cur_worker['location'] = '/data/mongodb/data/dbms1'
        elif worker.split(":")[1] == '8002':
            cur_worker['location'] = '/data/mongodb/data/dbms2'
        try:
            result = request_info(worker, {})
            print("result is : " + str(result))
            if not bool(result['success']):
                cur_worker['status'] = 'DOWN'
            else:
                worker_info = result['data']
                cur_worker['info'] = worker_info
                cur_worker['status'] = 'OK'
        except requests.exceptions.ConnectionError:
            # worker is down!
            cur_worker['status'] = 'DOWN'

        res.append(cur_worker)

    return {'Success': True,
            'data': res}
