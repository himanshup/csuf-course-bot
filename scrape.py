from dotenv import load_dotenv
load_dotenv()
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from os import environ
import re
import os
import time

CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
if environ.get('GOOGLE_CHROME_BIN') is not None:
    chrome_options.binary_location = os.environ['GOOGLE_CHROME_BIN']
url = 'https://mycsuf.fullerton.edu/psp/pfulprd/EMPLOYEE/CFULPRD/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?PORTALPARAM_PTCNAV=FUL_POC_SA_COURSE_CATALOG_SRCH'


def checkAvailability(subject, course):
    # Add optionƒ to run chrome in headless mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    try:
        driver = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        driver.get(url)
        # The content we want to scrape is in a frameset so we switch to the frame we want, which has the name TargetContent
        driver.switch_to.frame(driver.find_element_by_name('TargetContent'))

        # Select term (Spring 2019 for now, will add options for more terms later)
        select = Select(driver.find_element_by_id('CLASS_SRCH_WRK2_STRM$35$'))
        select.select_by_value('2193')

        time.sleep(1)
        try:
            select = Select(driver.find_element_by_id(
                'SSR_CLSRCH_WRK_SUBJECT_SRCH$0'))
            select.select_by_value(subject)
        except NoSuchElementException as exception:
            return "Couldn't find the subject " + subject + ", try again. (e.g. CPSC 121"

        # Select Course Career (undergrad only for now, more options later)
        select = Select(driver.find_element_by_id(
            'SSR_CLSRCH_WRK_ACAD_CAREER$2'))
        select.select_by_value('UGRD')

        inputElement = driver.find_element_by_id(
            'SSR_CLSRCH_WRK_CATALOG_NBR$1')
        inputElement.send_keys(course)

        searchButton = driver.find_element_by_id(
            'CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH')
        searchButton.click()

        time.sleep(1)
        soupLevel1 = BeautifulSoup(driver.page_source, 'lxml')
        rows = soupLevel1.findAll('table', {'class': 'PSLEVEL1GRIDNBONBO'})

        if len(rows) < 1:
            return 'No classes found'
        else:
            # Loop through all rows and append to one string so it sends in one message
            result = ''
            for index in range(len(rows)):
                time.sleep(2)
                driver.find_element_by_name(
                    'MTG_CLASSNAME$' + str(index)).click()
                time.sleep(2)
                soupLevel2 = BeautifulSoup(driver.page_source, 'lxml')
                status = soupLevel2.find('span',
                                         {'id': 'SSR_CLS_DTL_WRK_SSR_DESCRSHORT'}).text

                className = soupLevel2.find('span',
                                            {'id': 'DERIVED_CLSRCH_DESCR200'}).text
                classNum = soupLevel2.find('span',
                                           {'id': 'SSR_CLS_DTL_WRK_CLASS_NBR'}).text
                meetings = soupLevel2.find('span', {'id': 'MTG_SCHED$0'}).text
                instructor = soupLevel2.find('span',
                                             {'id': 'MTG_INSTR$0'}).text

                result += '\n\nClass: ' + className + '\nClass Number: ' + classNum + '\nStatus: ' + \
                    status + '\nDays & Times: ' + meetings + '\nInstructor: ' + instructor
                if status == 'Wait List':
                    capacity = soupLevel2.find('span',
                                               {'id': 'SSR_CLS_DTL_WRK_WAIT_CAP'}).text
                    total = soupLevel2.find('span',
                                            {'id': 'SSR_CLS_DTL_WRK_WAIT_TOT'}).text
                    print('Wait List Capacity: ' + capacity)
                    print('Wait List Total: ' + total)
                    result += ('\nWait List Capacity: ' + capacity +
                               '\nWait List Total: ' + total)
                else:
                    availableSeats = soupLevel2.find('span',
                                                     {'id': 'SSR_CLS_DTL_WRK_AVAILABLE_SEATS'}).text
                    result += ('\nAvailable Seats: ' + availableSeats)

                driver.find_element_by_name(
                    'CLASS_SRCH_WRK2_SSR_PB_BACK').click()

        driver.switch_to.default_content()
        driver.quit()
        return result
    except:
        driver.quit()
        return "An error occured."
