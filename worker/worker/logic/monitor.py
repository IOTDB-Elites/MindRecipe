import psutil

GB = 1024 * 1024 * 1024


def report():
    return {'success': True,
            'data': {'cpu': str(psutil.cpu_percent(interval=0.1, percpu=False)) + '%',
                     'memory': str(round(psutil.virtual_memory()[1] / GB, 4)) + ' GB',
                     'disk': str(round(psutil.disk_usage('/')[2] / GB, 4)) + ' GB'}}
