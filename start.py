#processing libraries
import threading
from subprocess import call
import sys 

def source():
    call([sys.executable, "jobs/job_source.py"]) 

def scraper():
    call([sys.executable, "jobs/job_scraper.py"])

def reset_scraper():
    call([sys.executable, "jobs/job_reset_scraper.py"])

# def classifier():
#     call([sys.executable, "jobs/job_classifier.py"]) 

process1 = threading.Thread(target=source)
process2 = threading.Thread(target=scraper)
process3 = threading.Thread(target=reset_scraper)
#process4 = threading.Thread(target=classifier)

process1.start()
process2.start()
process3.start()
#process4.start()