import os
import sys

current_path = os.path.abspath(__file__)
script_path = os.path.dirname(current_path)
project_path = os.path.dirname(script_path)

if project_path not in sys.path:
    sys.path.insert(0, project_path) 

from libs.sources import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

from seleniumbase import Driver

from bs4 import BeautifulSoup

import re

import random
def run(query, limit, headless=True):

    """
    Run the Google DE scraper.

    Args:
        query (str): The search query.
        limit (int): The maximum number of search results to retrieve.
        scraping: The Scraping object.

    Returns:
        list: List of search results.
    """
    try:
        #Definition of args for scraping the search engine
        search_url = "https://www.google.de/webhp?hl=de&gl=DE&&uule=w+CAIQICIHR2VybWFueQ==" #URL of search engine
        search_box = "q" #Class name of search box
        captcha = "g-recaptcha" #Source code hint for CAPTCHA
        next_page = "//a[@aria-label='{}']" #CSS to find click on next SERP
        next_scroll = "//span[@class='RVQdVd']"
        results_number = 0 #initialize results_number
        page = 1 #initialize SERP page
        search_results = [] #initialize search_results list
        get_search_url = "https://www.google.de/search?q="
        language = "&hl=de&gl=DE"

       


        #Definition of custom functions

        def search_pagination(source):
            soup = BeautifulSoup(source, features="lxml")
            if soup.find("span", class_=["SJajHc NVbCr"]):
                return True
            else:
                return False

        #Function to scrape search results
        def get_search_results(driver, page):

            get_search_results = []

            source = driver.page_source

            soup = BeautifulSoup(source, features="lxml")

            #addtional steps to extract undesired elements from the Search Engine Result Page (SERP)

            for s in soup.find_all("div", class_="d4rhi"):
                s.extract()

            for s in soup.find_all("div", class_="Wt5Tfe"):
                s.extract()

            for s in soup.find_all("div", class_="UDZeY fAgajc OTFaAf"):
                s.extract()

            #find the list with the search results by extracting the div container

            for result in soup.find_all("div", class_=["tF2Cxc", "dURPMd"]):
                url_list = []
                search_result = []
                result_title = ""
                result_description = ""
                result_url = ""
                try:
                    for title in result.find("h3", class_=["LC20lb MBeuO DKV0Md"]):
                        result_title+=title.text.strip()
                except:
                    result_title = "N/A"

                try:
                    for description in result.find("div", class_=re.compile("VwiC3b", re.I)):

                        result_description+=description.text.strip()
                except:
                    result_description = "N/A"

                try:
                    for url in result.find_all("a"):
                        url = url.attrs['href']
                        if "bing." in url:
                            url = get_real_url(url)
                        url_list.append(url)
                        result_url = url_list[0]
                except:
                    result_url = "N/A"

                if result_url != "N/A" and "http" in result_url:

                    get_search_results.append([result_url])                

               



            return get_search_results

        #Function to check if search engine shows CAPTCHA code
        def check_captcha(driver):
            source = driver.page_source
            if captcha in source:
                return True
            else:
                return False
            
        def remove_duplicates(search_results):

            cleaned_search_results = []

            i = 0

            url_list = {}

            for sr in search_results:
                url = sr[0]
                url_list[url] = i
                i = i + 1

            for key, value in url_list.items():                
                cleaned_search_results.append(search_results[value])

            
            return cleaned_search_results

        #initialize Selenium
        #https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/driver_manager.py For all options
        #https://seleniumbase.io/help_docs/locale_codes/
     

        driver = Driver(
                browser="chrome",
                wire=True,
                uc=True,
                headless2=headless,
                incognito=False,
                agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                do_not_track=True,
                undetectable=True,
                extension_dir=ext_path,
                locale_code="de",
                no_sandbox=True,
                )


        driver.set_page_load_timeout(60)
        driver.implicitly_wait(30)
        driver.get(search_url)
        random_sleep = random.randint(1, 2) #random timer trying to prevent quick automatic blocking
        time.sleep(random_sleep)

        if not check_captcha(driver):

            search = driver.find_element(By.NAME, search_box)
            search.send_keys(query)
            search.send_keys(Keys.RETURN)

            random_sleep = random.randint(1, 2)
            time.sleep(random_sleep)

            search_results = get_search_results(driver, page)

            search_results = remove_duplicates(search_results)


            results_number = len(search_results)

            print("first len search results: " +str(query) + " : "+str(results_number))

            if results_number == 0:
                driver.quit()
                random_sleep = random.randint(1, 2)
                time.sleep(random_sleep)                
                driver = Driver(
                browser="chrome",
                wire=True,
                uc=True,
                headless2=True,
                incognito=False,
                agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                do_not_track=True,
                undetectable=True,
                extension_dir=ext_path,
                locale_code="de",
                no_sandbox=True
                )
                                 


            if results_number < limit:       

                continue_scraping = True

                check_pagination = search_pagination(source = driver.page_source)

                if check_pagination:
                    print("pagination found")
                    #Click on next SERP pages as long the toal number of results is lower the limit
                    while (results_number <= limit) or page <= (limit / 10) and continue_scraping:
                        if not check_captcha(driver):
                            random_sleep = random.randint(1, 2)
                            time.sleep(random_sleep)
                            page+=1
                            page_label = f"Page {page}"
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            try:
                                next = driver.find_element(By.XPATH, next_page.format(page_label))
                                next.click()
                                search_results+= get_search_results(driver, page)
                                search_results = remove_duplicates(search_results)
                                results_number = len(search_results)
                            except:
                                continue_scraping = False
                        else:
                            continue_scraping = False
                            search_results = -1

                    driver.quit()

                    return search_results

                else:
                    print("no pagination")
                    SCROLL_PAUSE_TIME = 1
                    start = 0
                    query = query.lower()
                    get_query = query.replace(" ", "+")
                    search_results = []
                    results_number = 0


                    while (results_number <= limit and start <= limit) and continue_scraping:

                        if not check_captcha(driver):
                            try:
                                edit_search_url = get_search_url+get_query+language+"&start="+str(start)
                                print(edit_search_url)
                                driver.set_page_load_timeout(120)
                                driver.implicitly_wait(60)
                                driver.get(edit_search_url)
                                random_sleep = random.randint(2, 4) #random timer trying to prevent quick automatic blocking
                                time.sleep(random_sleep)
                                page+=1
                                start = start + 10
                                extract_search_results = get_search_results(driver, page)
                                print(len(extract_search_results))

                                if len(extract_search_results) > 0:
                                    print("go on")
                                    search_results+= extract_search_results

                                    search_results = remove_duplicates(search_results)

                                    results_number = len(search_results)

                                else:
                                    continue_scraping = False                                    
   

                            except Exception as e:
                                print(str(e))
                                continue_scraping = False
                        else:
                            continue_scraping = False
                            search_results = -1

                    driver.quit()
                                     
                    return search_results
            else:
                driver.quit()
                return search_results               


        else:
            search_results = -1
            driver.quit()

    except Exception as e:
        print(str(e))
        try:
            driver.quit()
        except:
            pass
        search_results = -1
        return search_results
