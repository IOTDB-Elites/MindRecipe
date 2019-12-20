import sched
import time
import os
from threading import Thread

import requests

from master.call_worker.http_request import request_heartbeat
from master.logic.metadata import workers
import multiprocessing
import subprocess

schedule = sched.scheduler(time.time, time.sleep)


def start_worker(worker):
    subprocess.Popen('./start_worker.sh ' + worker, shell=True, env={})


def send_heartbeat(inc):
    for worker in workers:
        try:
            request_heartbeat(worker)
        except requests.exceptions.ConnectionError:
            # worker is down!
            print('worker', worker, 'is down restarting...')
            start_worker(worker)
            # multiprocessing.Process(target=start_worker, args=(worker,)).start()
            print('start worker', worker)

    schedule.enter(inc, 0, send_heartbeat, (inc,))


def schedule_heartbeat(inc=10):
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    schedule.enter(inc, 0, send_heartbeat, (inc,))
    schedule.run()


def service(inc=5):
    Thread(target=schedule_heartbeat, args=(inc,)).start()
