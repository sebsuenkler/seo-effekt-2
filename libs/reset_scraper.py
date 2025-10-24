import sys

current_path = os.path.abspath(__file__)
script_path = os.path.dirname(current_path)
project_path = os.path.dirname(script_path)

if project_path not in sys.path:
    sys.path.insert(0, project_path) 

from libs.db import *

reset_ids = []

connection = connect_to_db()
cursor = connection.cursor()
data = cursor.execute("SELECT id FROM SCRAPER WHERE progress =?", (-1,))
connection.commit()
for row in data:
    id = row[0]
    reset_ids.append(id)

close_connection_to_db(connection)

if reset_ids:
    for r_id in reset_ids:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE SCRAPER SET progress =? WHERE id =?", (0,r_id,))
        connection.commit()
        close_connection_to_db(connection)
