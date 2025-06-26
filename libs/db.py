import sqlite3 as sl
import sys
import os

current_path = os.path.abspath(__file__)
script_path = os.path.dirname(current_path)
project_path = os.path.dirname(script_path)

if project_path not in sys.path:
    sys.path.insert(0, project_path) 


def connect_to_db():
    connection = sl.connect(project_path+'/seo_effect.db', timeout=10, isolation_level=None)
    connection.execute('pragma journal_mode=wal')
    return connection

def close_connection_to_db(connection):
    connection.close()
