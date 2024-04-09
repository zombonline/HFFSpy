from langdetect import detect
from steam import Steam
from decouple import config
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
from enum import Enum

KEY = config('STEAM_API_KEY')
steam = Steam(KEY)
url = f"https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"   

class WorkshopItem:
    def __init__(self, title, creator_id, creator_name, country, language, tus, rating, comment_count, date_posted, tags, item_type, creator_status):
        self.title = title
        self.creator_ID = creator_id
        self.creator_name = creator_name
        self.date_posted = date_posted
        self.country = country
        self.language = language 
        self.tus = tus
        self.rating = rating
        self.comment_count = comment_count
        self.tags = tags
        self.item_type = item_type
        self.creator_status = creator_status

def workshop_next_page(driver):
    currentPageUrl = driver.current_url
    currentPage = int(currentPageUrl.split('p=')[1])
    nextPage = currentPage + 1
    nextPageUrl = currentPageUrl.split('p=')[0] + 'p=' + str(nextPage)
    driver.get(nextPageUrl)

def get_total_items(driver):
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopBrowsePagingInfo')) > 0)
    except TimeoutException:
        print("Could not find expected number of items.")
        return 0
    total_items_string = driver.find_element(By.CSS_SELECTOR, 'div.workshopBrowsePagingInfo').text
    total_items = int(total_items_string.split('of ')[1].split(' ')[0].replace(',', ''))
    return total_items

def get_item_ids(driver, amount = None):
    wait = WebDriverWait(driver, 10)
    if amount is None:
        amount = get_total_items(driver)
    item_ids = []
    while len(item_ids) < amount:
        for item_css_element in driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem'):
            item_id = item_css_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('data-publishedfileid')
            item_ids.append(item_id)
        workshop_next_page(driver)
    return item_ids[:amount]
        
    # wait = WebDriverWait(driver, 10)
    # try:
    #     wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem')) > 0)
    # except TimeoutException:
    #     print("Timed out waiting for page to load")
    #     return []
    # item_ids = driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem').find_element(By.CSS_SELECTOR, 'a').get_attribute('data-publishedfileid')
    # return item_ids

class CreatorStatus(Enum):
    signed_creator = 1
    contacted_creator = 2
    pending_contact_creator = 3
    standard_creator = 4

def get_item_creator_status(creator_id):
    try:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        file = open(f"{this_dir}/CreatorStatus.txt", "r")
        for line in file:
            if creator_id in line:
                try:
                    return CreatorStatus(int(line.split('- ')[1]))
                except:
                    return CreatorStatus(4)
    except:
        return CreatorStatus(4)
def get_item_and_user_data(item_id):
    params = {
            'key': KEY,
            'itemcount': 1,
            'publishedfileids[0]': item_id
        }
    response = requests.post(url, data=params)
    data = response.json()
    workShopItem = data['response']['publishedfiledetails'][0]
    user = steam.users.get_user_details(data['response']['publishedfiledetails'][0]['creator'])
    return workShopItem, user
def create_workshop_item(item_id, driver):
    get_comments = False
    get_ratings = False
    workshop_item, user = get_item_and_user_data(item_id)
    title = get_item_title(workshop_item)
    creator_id = get_item_creator_id(workshop_item)
    creator_name = get_item_creator_name(user)
    country = get_item_creator_country(user)
    detected_language = get_item_creator_language(user, workshop_item)
    tus = get_item_tus(workshop_item)
    if get_ratings:
        rating = get_item_rating(workshop_item) 
    else:
        rating = "N/A"
    if get_comments:
        comment_count = get_item_comment_count(workshop_item, driver)
    else:
        comment_count = "N/A"
    date_posted = get_item_date_posted(workshop_item)
    tags = get_item_tags(workshop_item)
    item_type = get_item_type_from_tags(tags)
    creator_status = get_item_creator_status(creator_id)
    return WorkshopItem(title, creator_id, creator_name, country, detected_language, tus, rating, comment_count, date_posted, tags, item_type, creator_status)
def get_item_title(workshop_item):
    return workshop_item['title']
def get_item_creator_id(workshop_item):
    return workshop_item['creator']
def get_item_creator_name(user):
    if('personaname' in user['player']):
        return user['player']['personaname']
    else:
        return "N/A"
def get_item_creator_country(user):
    if('loccountrycode' in user['player']):
        return user['player']['loccountrycode']
    else:
        return "N/A"
def get_item_creator_language(user, workshop_item):
    #chinese override, if the user's country is already display as China, then the language is Chinese
    if(get_item_creator_country(user) == 'CN'):
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
def get_item_tus(workshop_item):
    return workshop_item['subscriptions']
def get_item_rating(workshop_item):
    return("N/A")
def get_item_comment_count(workshop_item, driver):
    wait = WebDriverWait(driver, 10)
    #get link to workshop item page via steam
    file_id = workshop_item["publishedfileid"]
    item_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={file_id}"
    driver.get(item_url)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "commentthread_count_label")))
        comment_count = driver.find_element(By.CLASS_NAME, "commentthread_count_label").text.split(' ')[0]
    except TimeoutException:
        comment_count = "0"
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return comment_count
def get_item_date_posted(workshop_item):
    date_string = "N/A"
    if('time_created' in workshop_item):
        date = datetime.fromtimestamp(workshop_item['time_created'])
        date_string = date.strftime("%d/%m/%Y")
    return date_string
def get_item_tags(workshop_item):
    tags = "N/A"
    if('tags' in workshop_item):
        tags = workshop_item['tags']
        tag_strings = [tag['tag'] for tag in tags]
        tag_string = ', '.join(tag_strings)
        return tag_string
    return tags
def get_item_type_from_tags(tags):
    if('Model' in tags):
        return "Model"
    elif('Levels' in tags):
        return "Level"
    elif('Lobbies' in tags):
        return "Lobby"
    else:
        return "N/A"

class Game:
    def __init__(self, appID, name, amountOfItems):
        self.appID = appID
        self.name = name
        self.amountOfItems = amountOfItems

def create_game_item(gameAppID, driver):
    gameName = steam.apps.get_app_details(gameAppID)[gameAppID]['data']['name']
    gameWorkShopItemCount = get_game_workshop_count(gameAppID, driver)
    newGame = Game(gameAppID, gameName, gameWorkShopItemCount)
    return newGame

def get_game_name(gameAppID):
    return steam.apps.get_app_details(gameAppID)[gameAppID]['data']['name']

def get_game_workshop_count(gameAppID, driver):
    wait = WebDriverWait(driver, 10)
    link = "https://steamcommunity.com/workshop/browse/?appid=" + gameAppID
    driver.get(link)
    gameWorkShopItemCount = "N/A"
    if gameAppID in driver.current_url:
        try:
            wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopBrowsePagingInfo')) > 0)
            itemCountText = driver.find_element(By.CSS_SELECTOR, 'div.workshopBrowsePagingInfo').text
            gameWorkShopItemCount = int(itemCountText.split('of ')[1].split(' entries')[0].replace(',', ''))
        except TimeoutException:
            print("Timed out waiting for page to load")
            return
    return gameWorkShopItemCount