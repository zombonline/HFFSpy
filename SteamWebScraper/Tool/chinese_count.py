import os
import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from steam import Steam
from datetime import datetime, timedelta
import xlsxwriter
import math
from decouple import config
from enum import Enum

import data_functions

other_asian_language_codes = ['id', 'ja', 'ko', 'th', 'tl', 'vi']

def get_workshop_link(start_date, end_date):
    link = f"https://steamcommunity.com/workshop/browse/?appid=477160&searchtext=&childpublishedfileid=0&browsesort=mostrecent&section=readytouseitems&created_date_range_filter_start={start_date}&created_date_range_filter_end={end_date}&updated_date_range_filter_start=0&updated_date_range_filter_end=0&p=1"
    return link

def create_workshop_item_objects_array(item_ids):
    item_objects = []
    for item_id in item_ids:
        item_object = data_functions.create_workshop_item(item_id, driver)
        item_objects.append(item_object)
    return item_objects
def write_to_excel(start_date, end_date, workshop_data):
    start_date = datetime.fromtimestamp(start_date)
    end_date = datetime.fromtimestamp(end_date)
    workbook = xlsxwriter.Workbook(f'UGCChineseSpeakingCount{start_date.strftime("%m-%d-%Y")}_to_{end_date.strftime("%m-%d-%Y")}.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Date Posted')
    worksheet.write('B1', 'Title')
    worksheet.write('C1', 'Creator Name')
    worksheet.write('D1', 'Type')
    worksheet.write('E1', 'Country')
    worksheet.write('F1', 'Language')

    chineseLevels = 0
    chineseModels = 0
    otherAsianLevels = 0
    otherAsianModels = 0
    totalLevels = 0
    totalModels = 0
    for(i, item) in enumerate(workshop_data):
        worksheet.write(i+1, 0, item.date_posted)
        worksheet.write(i+1, 1, item.title)
        worksheet.write(i+1, 2, item.creator_name)
        worksheet.write(i+1, 3, item.item_type)
        worksheet.write(i+1, 4, item.country)
        worksheet.write(i+1, 5, item.language)
        if 'zh' in item.language:
            if item.item_type == 'Level':
                chineseLevels += 1
            elif item.item_type == 'Model':
                chineseModels += 1
        elif item.language in other_asian_language_codes:
            if item.item_type == 'Level':
                otherAsianLevels += 1
            elif item.item_type == 'Model':
                otherAsianModels += 1
        if item.item_type == 'Level':
            totalLevels += 1
        elif item.item_type == 'Model':
            totalModels += 1
    worksheet.write('H2', 'Models')
    worksheet.write('H3', 'Chinese Entries')
    worksheet.write('H4', 'Other Asian Entries')
    worksheet.write('H5', 'Non-Asian Entries')

    worksheet.write('H7', 'Levels')
    worksheet.write('H8', 'Chinese Entries')
    worksheet.write('H9', 'Other Asian Entries')
    worksheet.write('H10', 'Non-Asian Entries')

    worksheet.write('H12', 'Total')
    worksheet.write('H13', 'Chinese Entries')
    worksheet.write('H14', 'Other Asian Entries')
    worksheet.write('H15', 'Non-Asian Entries')
    def percentage(part, whole):
        try:
            return part/whole
        except ZeroDivisionError:
            return 0

    worksheet.write('I2', totalModels)
    worksheet.write('I3', f"{chineseModels}")
    worksheet.write('J3', f"{percentage(chineseModels, totalModels):.2%}")
    worksheet.write('I4', f"{otherAsianModels}")
    worksheet.write('J4', f"{percentage(otherAsianModels, totalModels):.2%}")
    nonAsianModels = totalModels - chineseModels - otherAsianModels
    worksheet.write('I5', f"{nonAsianModels}")
    worksheet.write('J5', f"{percentage(nonAsianModels, totalModels):.2%}")

    worksheet.write('I7', totalLevels)
    worksheet.write('I8', f"{chineseModels}")
    worksheet.write('J8', f"{percentage(chineseLevels, totalLevels):.2%}")
    worksheet.write('I9', f"{otherAsianLevels}")
    worksheet.write('J9', f"{percentage(otherAsianLevels, totalLevels):.2%}")
    nonAsianLevels = totalLevels - chineseLevels - otherAsianLevels
    worksheet.write('I10', f"{nonAsianLevels}")
    worksheet.write('J10', f"{percentage(nonAsianLevels/totalLevels):.2%}")

    worksheet.write('I12', totalLevels + totalModels)
    worksheet.write('I13', f"{chineseLevels + chineseModels}")
    worksheet.write('J13', f"{percentage(chineseLevels + chineseModels, totalLevels + totalModels):.2%}")
    worksheet.write('I14', f"{otherAsianLevels + otherAsianModels}")    
    worksheet.write('J14', f"{:.2%}")
    nonAsianEntries = nonAsianLevels + nonAsianModels
    worksheet.write('I15', f"{nonAsianEntries}")
    worksheet.write('J15', f"{nonAsianEntries/(totalLevels + totalModels):.2%}")

    workbook.close()

KEY = config('STEAM_API_KEY')
steam = Steam(KEY)
url = f"https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"   

wait = None  
driver = None
def scan(d, start_date, end_date):
    global driver
    driver = d
    global wait
    wait = WebDriverWait(driver, 10)

    link = get_workshop_link(start_date, end_date)
    driver.get(link)

    workshop_data = []
    for item in create_workshop_item_objects_array(data_functions.get_item_ids(driver)):
        workshop_data.append(item)

    for item in workshop_data:
        write_to_excel(start_date, end_date, workshop_data)


