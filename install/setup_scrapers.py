"""
This script provides a basic test to verify the functionality of a scraper.

It is advisable to use this script to test scrapers before integrating them into RAT (Result Assessment Tool).
"""


import sys
import os

current_path = os.path.abspath(__file__)
script_path = os.path.dirname(current_path)
project_path = os.path.dirname(script_path)

if project_path not in sys.path:
    sys.path.insert(0, project_path) 

# Define the query for testing

test_query = 'test'

# Set headless to False to observe the Browser; Default is True

# Bing Test
from scrapers.bing_de_top10 import *
print("\n--- Microsoft Bing Test ---\n")
print(run(test_query, 10, True))

# Google Test
from scrapers.google_de_top10 import *
print("\n--- Google Test ---\n")
print(run(test_query, 10, True))