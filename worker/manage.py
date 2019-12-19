#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from worker.database import constant


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'worker.settings'
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    constant.port = sys.argv[3]
    execute_from_command_line(sys.argv[0:3])


if __name__ == '__main__':
    main()
