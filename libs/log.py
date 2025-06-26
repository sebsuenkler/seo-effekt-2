import sqlite3 as sl
import sys
import os

current_path = os.path.abspath(__file__)
script_path = os.path.dirname(current_path)
project_path = os.path.dirname(script_path)

if project_path not in sys.path:
    sys.path.insert(0, project_path)

def write_to_log(timestamp, content):
    f = open(project_path+"/tool.log", "a+")
    f.write(timestamp+": "+content+"\n")
    f.close()
