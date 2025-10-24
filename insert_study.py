import csv
import json
import sqlite3
import datetime

from libs.db import *


def adapt_date_iso(val):
    """Adapter to store a date as an ISO 8601 string."""
    return val.isoformat()

def convert_date(val):
    """Converter to parse an ISO 8601 date string back to a date object."""
    return datetime.date.fromisoformat(val.decode())

# Register the adapter and converter for handling 'date' types
sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_converter("date", convert_date)


today = datetime.date.today()
search_engines = []

try:
    with open('config/scraper.json') as json_file:
        search_engines_json = json.load(json_file)
except FileNotFoundError:
    print("Error: scraper.json not found. Please make sure the file exists.")
    exit() # Exit the script if config is missing

print("\n--- Form to Insert a New Study ---")
print()

name = ""
while not name:
    name = input("Insert the name of your study (required): ")

print()
description = input("Insert a description of your study (optional): ")
print()

print("--- Select Search Engines ---")
while not search_engines:
    for search_engine in search_engines_json:
        se_choice = ""
        while se_choice.lower() not in ["y", "n"]:
            se_choice = input(f"Do you want to scrape {search_engine} (y/n)?: ")
        if se_choice.lower() == "y":
            search_engines.append(search_engine)
    if not search_engines:
        print("You must select at least one search engine. Please try again.")

print()
queries = input("Enter the filepath to your queries file (default: queries.csv): ")
if not queries:
    queries = "queries.csv"
print()


# --- 2. PROCESS DATABASE TRANSACTION ---

# Open the database connection only ONCE.
connection = connect_to_db()
cursor = connection.cursor()

try:
    # First, check if a study with this name already exists.
    existing_study = cursor.execute("SELECT name FROM study WHERE name =?", (name,)).fetchone()

    if existing_study:
        print(f"Error: A study named '{name}' already exists. No changes were made.")
    else:
        # If no duplicate, proceed with creating the new study.
        print(f"Creating new study '{name}'...")

        # Insert the study record
        sql = 'INSERT INTO study(name, description, date) values(?,?,?)'
        data = (name, description, today)
        cursor.execute(sql, data)
        study_id = cursor.lastrowid

        # Process all queries from the CSV file
        with open(queries, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if not row: continue # Skip empty rows
                query = row[0]

                # Check for duplicate query within this specific study
                existing_query = cursor.execute("SELECT id FROM query WHERE query =? and study_id =?", (query, study_id)).fetchone()

                if not existing_query:
                    # Insert the new query record
                    sql = 'INSERT INTO query(study_id, query, date) values(?,?,?)'
                    data = (study_id, query, today)
                    cursor.execute(sql, data)
                    query_id = cursor.lastrowid

                    # For this new query, insert a scraper task for each selected search engine
                    for search_engine in search_engines:
                        sql = 'INSERT INTO scraper(study_id, query_id, query, search_engine, progress, date) values(?,?,?,?,?,?)'
                        data = (study_id, query_id, query, search_engine, 0, today)
                        cursor.execute(sql, data)
                else:
                    print(f"  - Query '{query}' already exists for this study (skipping).")

        # If all operations were successful, commit them to the database as a single transaction.
        connection.commit()
        print("\n--- Study successfully created and saved to the database! ---")

except FileNotFoundError:
    print(f"\nError: The queries file '{queries}' was not found.")
    print("Rolling back any changes. The database has not been modified.")
    connection.rollback()
except Exception as e:
    # If any error occurs during the 'try' block, roll back all changes.
    print(f"\nAn unexpected error occurred: {e}")
    print("Rolling back any changes. The database has not been modified.")
    connection.rollback()
finally:
    # This block always runs, ensuring the database connection is closed.
    close_connection_to_db(connection)
    print("Database connection closed.")