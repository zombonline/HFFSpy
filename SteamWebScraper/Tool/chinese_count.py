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
from langdetect import detect
import xlsxwriter
import math
from decouple import config
from enum import Enum
class WorkshopItem:
    def __init__(self, title, creator_ID, creator_name, country, detected_language, date_posted, tags, item_type):
        self.title = title
        self.creator_ID = creator_ID
        self.creator_name = creator_name
        self.detected_language = detected_language
        self.country = country
        self.date_posted = date_posted
        self.tags = tags
        self.item_type = item_type

def set_workshop_tags(tags):
    wait.until(lambda driver: driver.find_elements(By.CSS_SELECTOR, 'filterOption') > 0)
    for tag in tags:
        for option in driver.find_elements(By.CSS_SELECTOR, 'filterOption'):
            if tag in option.text:
                option.click()
                time.sleep(1)
                break            
def get_workshop_link(start_date, end_date):
    link = f'https://steamcommunity.com/workshop/browse/?appid=477160&searchtext=&childpublishedfileid=0&browsesort=trend&section=readytouseitems&created_date_range_filter_start={start_date}&created_date_range_filter_end={end_date}&updated_date_range_filter_start=NaN&updated_date_range_filter_end=NaN'
    return link
def get_workshop_css_elements():
    try:
        wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem')) > 0)
    except TimeoutException:
        print("Timed out waiting for page to load")
        return []
    workshop_css_elements = driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem')
    return workshop_css_elements
def get_steam_data_from_workshop_css_element(item):
    params = {
            'key': KEY,
            'itemcount': 1,
            'publishedfileids[0]': item.find_element(By.CSS_SELECTOR, 'a').get_attribute('data-publishedfileid')
        }
    response = requests.post(url, data=params)
    data = response.json()
    workShopItem = data['response']['publishedfiledetails'][0]
    user = steam.users.get_user_details(data['response']['publishedfiledetails'][0]['creator'])
    return workShopItem, user
def create_workshop_item_objects_array(workshop_css_elements):
    workshopItems = []
    for workshop_css_element in workshop_css_elements:
        workshop_item, user = get_steam_data_from_workshop_css_element(workshop_css_element)
        #Get Title of workshop item
        title = workshop_item['title']
        #Get AuthorID of workshop item
        creator_id = workshop_item['creator']
        #Get Author Name of workshop item
        creator_name = user['player']['personaname']
        #Get Country of Author
        country = get_user_country(user)
        #Get language of workshop item
        detected_language = get_langauge_from_user_and_item(user, workshop_item)
        #Get date posted of workshop item
        date_posted = datetime.fromtimestamp(workshop_item['time_created'])
        #Get tags of workshop item
        tags = get_tags(workshop_item['tags'])
        #Get type of workshop item ("Model" or "Level")
        item_type = get_item_type_from_tags(tags)
        #create a new workshop item object and append it to list.
        workshopItems.append(WorkshopItem(title, creator_id, creator_name, country, detected_language, date_posted, tags, item_type))
    return workshopItems
def get_user_country(user):
    if('loccountrycode' in user['player']):
        return user['player']['loccountrycode']
    else:
        return "N/A"
def get_langauge_from_user_and_item(user, workshop_item):
    #chinese override, if the user's country is already display as China, then the language is Chinese
    if(get_user_country(user) == 'CN'):
        return 'zh-cn'
    strings = []
    if user is None:
        pass
    else:
        if('personaname' in user['player']):
            strings.append(user['player']['personaname'])
        if('realname' in user['player']):
            strings.append(user['player']['realname'])
        if('bio' in user['player']):
            strings.append(user['player']['bio'])
    if workshop_item is None:
        pass
    else:
        if('title' in workshop_item):
            strings.append(workshop_item['title'])
        if('description' in workshop_item):
            strings.append(workshop_item['description'])
    newString = ""
    for string in strings:
        newString = newString + ", " + string
    try:
        detected_language = detect(newString)
    except:
        detected_language = "N/A"

    #Chinese override (Example: if a player has a chinese username, but is using english in title/description of the item,
    #the language might be detected as english, but we want to override that and set it to chinese)
    if 'zh' not in detected_language:
        for string in strings:
            try:
                if 'zh' in detect(string):
                    detected_language = 'zh-cn'
                    break
            except:
                continue
    return detected_language
def get_tags(tags):
    tag_strings = [tag['tag'] for tag in tags]
    tag_string = ', '.join(tag_strings)
    return tag_string
def get_item_type_from_tags(tags):
    if('Model' in tags):
        return "Model"
    elif('Levels' in tags):
        return "Level"
    elif('Lobbies' in tags):
        return "Lobby"
    else:
        return "N/A"
def write_to_excel(start_date, end_date, week, workshop_data):
    workbook = xlsxwriter.Workbook(f'chinese proportion {start_date.strftime('%y')} week {week}.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('B1', f'Week {week}')
    worksheet.write('B2', f'{start_date.strftime("%d/%m")} - {end_date.strftime("%d/%m")}')
    worksheet.write('B3', f'''
                    First Item: {workshop_data[0].title} by {workshop_data[0].creator_name}
                    Last Item: {workshop_data[-1].title} by {workshop_data[-1].creator_name}''')
    worksheet.write('A4', 'Worldwide Items')
    worksheet.write('B4', str(len(workshop_data)))
    chineseCount = 0
    for item in workshop_data:
        if 'zh' in item.detected_language:
            chineseCount += 1
    worksheet.write('A5', 'Chinese Items')
    worksheet.write('B5', str(chineseCount))
    percentage = (chineseCount/len(workshop_data)) * 100
    worksheet.write('A6', 'Chinese Proportion')
    worksheet.write('B6', f'{round(percentage)}%')
    workbook.close()


start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 1, 7)
tags = []
driver = None
wait = WebDriverWait(driver, 10)

