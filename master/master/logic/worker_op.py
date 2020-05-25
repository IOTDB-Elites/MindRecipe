import socket
import subprocess
import time

from master.call_worker import http_request
from master.logic import metadata


def is_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


def add_worker(ip, port):
    print(ip)
    print(port)
    metadata.workers.append(ip)
    metadata.workers_port.append(port)
    # subprocess.Popen('/home/fit/reading/start_worker.sh ' + ip + ' ' + port, shell=True, env={})
    print(metadata.workers)
    # time.sleep(5)
    return {
        'success': True,
        'message': 'assigned port: ' + str(port),
        'data': {}
    }


def remove_worker(ip):
    metadata.workers.pop()
    metadata.workers_port.pop()
    res = http_request.remove_dbms(ip, {})
    return {'success': True}
