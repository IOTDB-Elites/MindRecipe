import sched
import time
import os
from threading import Thread

import requests

from master.call_worker.http_request import request_heartbeat
from master.logic.metadata import workers, workers_port
import multiprocessing
import subprocess

schedule = sched.scheduler(time.time, time.sleep)


def start_worker(worker, port):
    subprocess.Popen(['./start_worker.sh', worker, port], shell=False, env={})


def send_heartbeat(inc):
    for i in range(len(workers)):
        worker = workers[i]
        res = request_heartbeat(worker)
        if not res['success']:
            print(res)
            print('worker', worker, 'is down restarting...')
            port = workers_port[i]
            start_worker(worker, port)
            # multiprocessing.Process(target=start_worker, args=(worker,)).start()
            print('start worker', worker)

    schedule.enter(inc, 0, send_heartbeat, (inc,))


def schedule_heartbeat(inc=10):
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    schedule.enter(inc, 0, send_heartbeat, (inc,))
    schedule.run()


def service(inc=5):
    Thread(target=schedule_heartbeat, args=(inc,)).start()
