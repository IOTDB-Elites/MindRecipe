import subprocess
import random
import time
import socket
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
    server_port = random.randint(8000, 9000)
    worker = ip + ":" + str(server_port)
    subprocess.Popen('./start_worker.sh ' + worker + ' ' + port, shell=True, env={})
    metadata.workers.append(worker)
    time.sleep(5)
    return {
        'success': True,
        'message': 'assigned port: ' + str(port),
        'data': {}
    }
