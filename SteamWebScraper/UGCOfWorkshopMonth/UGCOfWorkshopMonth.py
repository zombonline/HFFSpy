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
from datetime import datetime
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
        self.tus = tus
        self.rating = rating
        self.comment_count = comment_count
        self.date_posted = date_posted
        self.creator_status = creator_status  
        self.country = country
        self.language = language   
def user_define_date_range():
    m = input("Please enter the month of the data you want to scrape (MM): ")
    y = input("Please enter the year of the data you want to scrape (YYYY): ")
    start_date = round(datetime(int(y), int(m), 1, 0, 0, 0).timestamp())
    end_date = None
    last_day = 31
    while end_date == None:
        try:
            end_date = round(datetime(int(y), int(m), last_day, 23, 59, 59).timestamp())
        except ValueError:
            last_day -= 1
    if(end_date > round(datetime.now().timestamp())):
        end_date = round(datetime.now().timestamp())
    print(f"Start Date: {datetime.fromtimestamp(start_date)} - End Date: {datetime.fromtimestamp(end_date)}")
    return start_date,end_date
def get_item_comment_count(item):
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
def output_to_excel(list):
    month = datetime.fromtimestamp(start_date).month
    year = datetime.fromtimestamp(start_date).year
    workbook = xlsxwriter.Workbook(f'UGCOfWorkshopMonth {year}-{month}.xlsx')
    worksheet = workbook.add_worksheet(f"{year} {month}")
    bold = workbook.add_format({'bold': True})
    hilight_orange = workbook.add_format({'bg_color': 'orange'})
    hilight_green = workbook.add_format({'bg_color': 'green'})
    hilight_yellow = workbook.add_format({'bg_color': 'yellow'})
    worksheet.write('A1', 'Name of the level', bold)
    worksheet.write('B1', 'Creator', bold)
    worksheet.write('C1', 'Country', bold)
    worksheet.write('D1', 'Language', bold)
    worksheet.write('E1', f'TUS ({ datetime.now().strftime("%d/%m/%Y")})', bold)
    worksheet.write('F1', 'Rating', bold)
    worksheet.write('G1', 'Comments', bold)
    worksheet.write('H1', 'Date Posted', bold)
    worksheet.write('J3', 'Signed Creator', hilight_orange)
    worksheet.write('J4', 'Creator we have contacted', hilight_green)
    worksheet.write('J5', 'Creator we are planning to approach', hilight_yellow)
    row = 1
    col = 0
    for item in list:
        worksheet.write(row, col, item.title)
        if item.creator_status == CreatorStatus.signed_creator:
            worksheet.write(row, col + 1, item.creator_name, hilight_orange)
        elif item.creator_status == CreatorStatus.contacted_creator:
            worksheet.write(row, col + 1, item.creator_name, hilight_green)
        elif item.creator_status == CreatorStatus.pending_contact_creator:
            worksheet.write(row, col + 1, item.creator_name, hilight_yellow)
        else:
            worksheet.write(row, col + 1, item.creator_name)
        worksheet.write(row, col + 2, item.country)
        worksheet.write(row, col + 3, item.language)
        worksheet.write(row, col + 4, item.tus)
        worksheet.write(row, col + 5, item.rating)
        worksheet.write(row, col + 6, item.comment_count)
        worksheet.write(row, col + 7, item.date_posted.strftime("%d/%m/%Y"))

        row += 1
    workbook.close()
def ExtractWorkShopData():
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "workshopItem")))
    workshopItems = driver.find_elements(By.CLASS_NAME, "workshopItem")
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
        item_comment_count = get_item_comment_count(item)
        item_date_posted = datetime.fromtimestamp(item_data['response']['publishedfiledetails'][0]['time_created'])
        creatorID = item_data['response']['publishedfiledetails'][0]['creator']
        item_creator_status = GetCreatorStatus(creatorID)
        item_creator_country = get_user_country(steam.users.get_user_details(creatorID))
        item_creator_language = get_langauge_from_user_and_item(steam.users.get_user_details(creatorID), item_data['response']['publishedfiledetails'][0])
        item = WorkshopItem(item_title, item_creator_name, item_creator_country, item_creator_language, item_TUS, item_rating, item_comment_count, item_date_posted, item_creator_status)
        workshop_data.append(item)
    return workshop_data
def GetCreatorStatus(creator_ID):
    file = open("CreatorStatus.txt", "r")
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
        
#region ChromeDriver 
options = Options()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--log-level=3")
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
chrome_driver_path = os.path.join(base_dir, "chromedriver.exe")
print(f"Looking for ChromeDriver at {chrome_driver_path}")
if not os.path.exists(chrome_driver_path):
    print("ChromeDriver not found. Please download the latest version of ChromeDriver from https://sites.google.com/chromium.org/driver/ and place it in the same directory as this script.")
    input("Press Enter to close the program...")
    sys.exit(1)
webdriver_service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=webdriver_service, options=options)
wait = WebDriverWait(driver, 3)
#endregion

start_date, end_date = user_define_date_range()
link = f"https://steamcommunity.com/workshop/browse/?appid=477160&browsesort=trend&section=readytouseitems&requiredtags%5B0%5D=Levels&created_date_range_filter_start={start_date}&created_date_range_filter_end={end_date}&updated_date_range_filter_start=NaN&updated_date_range_filter_end=NaN&actualsort=trend&p=1&days=-1"


driver.get(link)
workshop_data = ExtractWorkShopData()
output_to_excel(workshop_data)


