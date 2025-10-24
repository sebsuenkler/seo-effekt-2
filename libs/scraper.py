
import os
import sys

current_path = os.path.abspath(__file__)
script_path = os.path.dirname(current_path)
project_path = os.path.dirname(script_path)

if project_path not in sys.path:
    sys.path.insert(0, project_path) 

ext_path = project_path+"/i_care_about_cookies_unpacked"

import datetime

import json

import importlib


current_path = os.path.abspath(__file__)
script_path = os.path.dirname(current_path)
project_path = os.path.dirname(script_path)

if project_path not in sys.path:
    sys.path.insert(0, project_path) 


from libs.sources import get_real_url

from libs.db import *
from libs.log import *

scraper_id = 0
reset_id = 0

import json

connection = connect_to_db()
cursor = connection.cursor()
data = cursor.execute("SELECT id FROM scraper WHERE progress =? ORDER BY RANDOM() LIMIT 1", (-1,))
connection.commit()
for row in data:
    reset_id = row[0]

close_connection_to_db(connection)

if reset_id == 0:

    connection = connect_to_db()
    cursor = connection.cursor()
    data = cursor.execute("SELECT * FROM scraper WHERE progress =? ORDER BY RANDOM() LIMIT 1", (0,))
    connection.commit()

    for row in data:
        scraper_id = row[0]
        study_id = row[1]
        query_id = row[2]
        query = row[3]
        search_engine = row[4]
    close_connection_to_db(connection)

    if scraper_id != 0:

        timestamp = datetime.datetime.now()
        timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

        write_to_log(timestamp, "Scrape "+str(search_engine)+" Job_Id:"+str(scraper_id)+" Query:"+str(query)+" started")

        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE scraper SET progress =? WHERE id =?", (2,scraper_id,))
        connection.commit()
        close_connection_to_db(connection)


        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys

        import time

        from seleniumbase import Driver

        from lxml import html
        from bs4 import BeautifulSoup

        import json

        with open(project_path+'/config/scraper.json') as json_file:
            search_engines_json = json.load(json_file)

        try:

            scraper_lib = search_engines_json[search_engine]['scraper_file'] 
            limit = search_engines_json[search_engine]['limit']
            module_path_for_import = f"scrapers.{scraper_lib}"
            scraper = importlib.import_module(module_path_for_import)

            search_results = scraper.run(query, limit)

            if search_results == -1:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("UPDATE scraper SET progress =? WHERE id =?", (-1,scraper_id,))
                connection.commit()
                close_connection_to_db(connection)

                timestamp = datetime.datetime.now()
                timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

                write_to_log(timestamp, "Scrape "+str(search_engine)+" Job_Id:"+str(scraper_id)+" Query:"+str(query)+" failed [CAPTCHA]")

            else:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("UPDATE scraper SET progress =? WHERE id =?", (1,scraper_id,))
                connection.commit()
                close_connection_to_db(connection)

                timestamp = datetime.datetime.now()
                timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

                write_to_log(timestamp, "Scrape "+str(search_engine)+" Job_Id:"+str(scraper_id)+" Query:"+str(query)+" success")


                import datetime
                from datetime import date
                today = date.today()
                timestamp = datetime.datetime.now()

                from urllib.parse import urlsplit
                from urllib.parse import urlparse
                import socket

                def get_meta(url):
                    meta = []
                    try:
                        parsed_uri = urlparse(url)
                        hostname = '{uri.netloc}'.format(uri=parsed_uri)
                        ip = socket.gethostbyname(hostname)
                    except:
                        ip = "-1"

                    main = '{0.scheme}://{0.netloc}/'.format(urlsplit(url))
                    meta = [ip, main]
                    return meta

                position = 0

                for urls in search_results:

                    for url in urls:

                        meta = get_meta(url)

                        ip = meta[0]
                        main_url = meta[1]

                        position+=1

                        if position <= limit:

                            connection = connect_to_db()
                            cursor = connection.cursor()
                            sql = 'INSERT INTO search_result(study_id, query_id, scraper_id, ip, search_engine, position, url, main_url, timestamp, date) values(?,?,?,?,?,?,?,?,?,?)'
                            data = (study_id, query_id, scraper_id, ip, search_engine, position, url, main_url, timestamp, today)
                            cursor.execute(sql, data)
                            connection.commit()
                            result_id = cursor.lastrowid
                            close_connection_to_db(connection)

                            connection = connect_to_db()
                            cursor = connection.cursor()
                            sql = 'INSERT INTO source(result_id, scraper_id, progress, date) values(?,?,?,?)'
                            data = (result_id, scraper_id, 0, today)
                            cursor.execute(sql, data)
                            connection.commit()
                            close_connection_to_db(connection)
        except Exception as e:
            print(str(e))
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("UPDATE scraper SET progress =? WHERE id =?", (-1,scraper_id,))
            connection.commit()
            close_connection_to_db(connection)

            timestamp = datetime.datetime.now()
            timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

            write_to_log(timestamp, "Scrape "+str(search_engine)+" Job_Id:"+str(scraper_id)+" Query:"+str(query)+" failed")
