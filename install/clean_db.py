import sys
import os

current_path = os.path.abspath(__file__)
script_path = os.path.dirname(current_path)
project_path = os.path.dirname(script_path)

if project_path not in sys.path:
    sys.path.insert(0, project_path) 

from libs.db import *

connection = connect_to_db()
if connection:
    connection.execute('VACUUM;')
    print("VACUUM excecuted.")
    close_connection_to_db(connection)
else:
    print("Connection to DB failed")