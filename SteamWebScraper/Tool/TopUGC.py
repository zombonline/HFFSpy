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
from datetime import datetime, date
from langdetect import detect
import xlsxwriter
import math
from decouple import config
from enum import Enum

class CreatorStatus(Enum):
    signed_creator = 1
    contacted_creator = 2
    pending_contact_creator = 3
    standard_creator = 4
class WorkshopItem:
    def __init__(self, title, creator_name, country, language, tus, rating, comment_count, date_posted, creator_status):
        self.title = title
        self.creator_name = creator_name
        self.date_posted = date_posted
        self.country = country
        self.language = language 
        self.tus = tus
        self.rating = rating
        self.comment_count = comment_count
        self.creator_status = creator_status    
def get_item_comment_count(item, driver, wait):
    item_url = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    driver.execute_script(f"window.open('{item_url}');")
    driver.switch_to.window(driver.window_handles[1])
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "commentthread_count_label")))
        comment_count = driver.find_element(By.CLASS_NAME, "commentthread_count_label").text.split(' ')[0]
    except TimeoutException:
        comment_count = "0"
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return comment_count
def output_to_excel(level_list, model_list):
    workbook = xlsxwriter.Workbook('UGCOfWorkshopMonth.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Level')
    worksheet.write('A2', 'Rank')
    worksheet.write('B2', 'Title')
    worksheet.write('C2', 'Creator')
    worksheet.write('D2', 'Date Posted')
    worksheet.write('E2', 'Country')
    worksheet.write('F2', 'Language')
    worksheet.write('G2', f'TUS ({date.today()})')
    worksheet.write('H2', 'Rating')
    worksheet.write('I2', 'Comment Count')
    worksheet.write('A23', 'Model')
    worksheet.write('A24', 'Rank')
    worksheet.write('B24', 'Title')
    worksheet.write('C24', 'Creator')
    worksheet.write('D24', 'Date Posted')
    worksheet.write('E24', 'Country')
    worksheet.write('F24', 'Language')
    worksheet.write('G24', f'TUS ({date.today()})')
    worksheet.write('H24', 'Rating')
    worksheet.write('I24', 'Comment Count')

    for i in range(len(level_list)):
        worksheet.write(i+2, 0, i+1)
        worksheet.write(i+2, 1, level_list[i].title)
        worksheet.write(i+2, 2, level_list[i].creator_name)
        worksheet.write(i+2, 3, level_list[i].date_posted.strftime("%m/%d/%Y, %H:%M:%S"))
        worksheet.write(i+2, 4, level_list[i].country)
        worksheet.write(i+2, 5, level_list[i].language)
        worksheet.write(i+2, 6, level_list[i].tus)
        worksheet.write(i+2, 7, level_list[i].rating)
        worksheet.write(i+2, 8, level_list[i].comment_count)
    for i in range(len(model_list)):
        worksheet.write(i+24, 0, i+1)
        worksheet.write(i+24, 1, model_list[i].title)
        worksheet.write(i+24, 2, model_list[i].creator_name)
        worksheet.write(i+24, 3, model_list[i].date_posted.strftime("%m/%d/%Y, %H:%M:%S"))
        worksheet.write(i+24, 4, model_list[i].country)
        worksheet.write(i+24, 5, model_list[i].language)
        worksheet.write(i+24, 6, model_list[i].tus)
        worksheet.write(i+24, 7, model_list[i].rating)
        worksheet.write(i+24, 8, model_list[i].comment_count)
    workbook.close()
    
def ExtractWorkShopData(driver, wait):
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "workshopItem")))
    workshopItems = driver.find_elements(By.CLASS_NAME, "workshopItem")
    if(len(workshopItems) > 20):
        workshopItems = workshopItems[:20]
    workshop_data = []
    for item in workshopItems:
        params = {
                'key': KEY,
                'itemcount': 1,
                'publishedfileids[0]': item.find_element(By.CSS_SELECTOR, 'a').get_attribute('data-publishedfileid')
            }
        response = requests.post(url, data=params)
        item_data = response.json()
        print(steam.users.get_user_details(item_data['response']['publishedfiledetails'][0]['creator']))
        item_title = item_data['response']['publishedfiledetails'][0]['title']
        item_creator_name = steam.users.get_user_details(item_data['response']['publishedfiledetails'][0]['creator'])['player']['personaname']
        item_TUS = item_data['response']['publishedfiledetails'][0]['lifetime_subscriptions']
        item_rating = 'N/A (Needs log in)'
        item_comment_count = get_item_comment_count(item, driver, wait)
        item_date_posted = datetime.fromtimestamp(item_data['response']['publishedfiledetails'][0]['time_created'])
        creatorID = item_data['response']['publishedfiledetails'][0]['creator']
        item_creator_status = GetCreatorStatus(creatorID)
        item_creator_country = get_user_country(steam.users.get_user_details(creatorID))
        item_creator_language = get_langauge_from_user_and_item(steam.users.get_user_details(creatorID), item_data['response']['publishedfiledetails'][0])
        item = WorkshopItem(item_title, item_creator_name, item_creator_country, item_creator_language, item_TUS, item_rating, item_comment_count, item_date_posted, item_creator_status)
        workshop_data.append(item)
    return workshop_data
def GetCreatorStatus(creator_ID):
    this_dir = os.path.dirname(os.path.abspath(__file__))

    file = open(f"{this_dir}/CreatorStatus.txt", "r")
    for line in file:
        if creator_ID in line:
            try:
                return CreatorStatus(int(line.split('- ')[1]))
            except:
                return CreatorStatus(4)
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

KEY = config('STEAM_API_KEY')
steam = Steam(KEY)
url = f"https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"   
        
def scan(driver, wait, start_date, end_date, amount_of_items):
    print("Scanning for top UGC of the month...")
    print(f"From {start_date} to {end_date}")
    print(f"Amount of items to scan: {amount_of_items}")
    level_link = f"https://steamcommunity.com/workshop/browse/?appid=477160&browsesort=trend&section=readytouseitems&requiredtags%5B0%5D=Levels&created_date_range_filter_start={start_date}&created_date_range_filter_end={end_date}&updated_date_range_filter_start=NaN&updated_date_range_filter_end=NaN&actualsort=trend&p=1&days=-1"
    driver.get(level_link)
    level_workshop_data = ExtractWorkShopData(driver, wait)

    model_link = f"https://steamcommunity.com/workshop/browse/?appid=477160&browsesort=trend&section=readytouseitems&requiredtags%5B0%5D=Model&created_date_range_filter_start={start_date}&created_date_range_filter_end={end_date}&updated_date_range_filter_start=NaN&updated_date_range_filter_end=NaN&actualsort=trend&p=1&days=-1"
    driver.get(model_link)
    model_workshop_data = ExtractWorkShopData(driver, wait)
    output_to_excel(level_workshop_data, model_workshop_data)

