#!/usr/env/bin/ python3.6

from bs4 import BeautifulSoup

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

import urllib3

import logging
import sys

import logging.config

import certifi

import pandas as pd



#from user_agent import generate_user_agent



def scrap_main_page(url='https://www.flashscore.com/football/france/ligue-1/fixtures/'):

    """

    :return: the list of code associated to each game

    """
    try:
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                   ca_certs=certifi.where())

        page_response = http.request('GET', url, timeout=2.5, retries=False)

    except urllib3.exceptions.HTTPError as e:
        logger.error(msg=e)
        #raise
        sys.exit(1)
    # print(page_response.status_code)


    page_content = BeautifulSoup(page_response.data, 'html.parser')

    #print(page_content.prettify())
    # extract all html elements where game is store

    # game = page_content.find_all(class='padl')

    odd_stage_scheduled = page_content.find(id='tournament-page-data-fixtures')
    odd_stage_scheduled = odd_stage_scheduled.get_text()


    id = re.compile('(?<=AA÷)\w+(?=¬AD÷)')

    res = id.findall(odd_stage_scheduled)

    return res



def process_content(id):
    '''

     Return the odds for the game associated with the id
    :param id:
    :return:
    '''

    try:
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                   ca_certs=certifi.where())

        url = 'https://www.flashscore.com/match/{}/#odds-comparison;1x2-odds;full-time'.format(id)

        page_response = http.request('GET', url, timeout=2.5, retries=False)
        page_content = BeautifulSoup(page_response.data, 'html.parser')
        #print(page_content.prettify())
        return page_content

    except urllib3.exceptions.HTTPError as e:

        logger.error(msg=e)

        sys.exit(1)





import numpy as np
import pandas as pd
import datetime

if __name__ == '__main__':
    try:
        print('\nProcessing.....')
        game_id = scrap_main_page()
        [print(i) for i in game_id]
        #process_content(game_id[0])

        id_ = game_id[0]
        url_full_time = 'https://www.flashscore.com/match/{}/#odds-comparison;1x2-odds;full-time'.format(id_)
        print(url_full_time)
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)
        driver.get(url_full_time)
        odd_values = driver.find_elements_by_class_name('odds-table-wrapper')
        #TODO: Grab event  date
        #TODO: TEAM NAME
        # TODO: datetime of query
        #TODO : save object ion a dictionary with the bookmaker as key

        #res = driver.findElement(By.className("odds-table-wrapper"))

        vec = odd_values[0].text

        size = len(vec)-1

        res = list(map(float, vec.splitlines()[2:size]))

        A = np.array(res)

        result = np.reshape(A, (-1,3))

        #result for each bookmaker
        print('\n result for one game\n')
        data = pd.DataFrame(data=result.tolist())
       # print(result.tolist())

        print(data)

        today = datetime.datetime.today()

        driver.close()
        driver.stop_client()

    except ValueError:
        raise
        sys.exit(1)

