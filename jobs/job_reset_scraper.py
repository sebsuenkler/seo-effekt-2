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
    os.system('python libs/reset_scraper.py')

if __name__ == '__main__':

    first_run = datetime.datetime.now() + datetime.timedelta(seconds=1200)

    scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone='Europe/Berlin')
    scheduler.add_job(job, 'interval', seconds=1200, next_run_time=first_run)
    scheduler.start()

    time.sleep(3)

    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")
    write_to_log(timestamp, "Job_Reset_Scraper started")

    print(f"Job_Reset_Scraper started at {timestamp}")

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
