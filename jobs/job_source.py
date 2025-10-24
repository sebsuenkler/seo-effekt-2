#processing libraries
import threading
import importlib
from subprocess import call
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import datetime
import sys

current_path = os.path.abspath(__file__)
script_path = os.path.dirname(current_path)
project_path = os.path.dirname(script_path)

if project_path not in sys.path:
    sys.path.insert(0, project_path) 

from libs.log import *

job_defaults = {
    'coalesce': False,
    'max_instances': 2
}

def job():
    os.system('python libs/source.py')

if __name__ == '__main__':
    scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone='Europe/Berlin')
    scheduler.add_job(job, 'interval', seconds=120, next_run_time=datetime.datetime.now())
    scheduler.start()

    time.sleep(2)

    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

    write_to_log(timestamp, "Job_Source started")

    print(f"Job_Source started at {timestamp}")


    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
