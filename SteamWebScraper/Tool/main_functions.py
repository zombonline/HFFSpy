import time
from langdetect import detect
from steam import Steam
from decouple import config
import requests
import sys
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
driver = None
wait = None

def start_driver():
    global driver
    global wait
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    if(get_setting_value("display_browser") == 0):
        options.add_argument("--headless")
        print("No browser will be displayed")
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    chrome_driver_path = os.path.join(base_dir, "chromedriver.exe")
    print(f"Looking for ChromeDriver at {chrome_driver_path}")
    if not os.path.exists(chrome_driver_path):
        print("ChromeDriver not found. Please download the latest version of ChromeDriver from https://sites.google.com/chromium.org/driver/ and place it in the same directory as this script.")
        input("Press Enter to close the program...")
        return False
    webdriver_service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=webdriver_service, options=options)
    wait = WebDriverWait(driver, 10)
    return driver


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

def workshop_next_page():
    currentPageUrl = driver.current_url
    currentPage = int(currentPageUrl.split('p=')[1])
    nextPage = currentPage + 1
    nextPageUrl = currentPageUrl.split('p=')[0] + 'p=' + str(nextPage)
    driver.get(nextPageUrl)

def get_total_items():
    try:
        wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopBrowsePagingInfo')) > 0)
    except TimeoutException:
        print("Could not find expected number of items.")
        return 0
    total_items_string = driver.find_element(By.CSS_SELECTOR, 'div.workshopBrowsePagingInfo').text
    total_items = int(total_items_string.split('of ')[1].split(' ')[0].replace(',', ''))
    return total_items

def get_item_ids(amount = None):
    if amount is None:
        amount = get_total_items()
    item_ids = []
    maxItemsFound = False
    while len(item_ids) < amount and maxItemsFound == False:
        for item_css_element in driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem'):
            item_id = item_css_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('data-publishedfileid')
            item_ids.append(item_id)
        workshop_next_page()
        try:
            wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem')) > 0)
        except:
            print("No items on page.")
        maxItemsFound = len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem')) == 0
    return item_ids[:amount]

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

def create_workshop_item(item_id):
    workshop_item, user = get_item_and_user_data(item_id)
    title = get_item_title(workshop_item)
    creator_id = get_item_creator_id(workshop_item)
    creator_name = get_item_creator_name(user)
    country = get_item_creator_country(user)
    detected_language = get_item_creator_language(user, workshop_item)
    tus = get_item_tus(workshop_item)
    date_posted = get_item_date_posted(workshop_item)
    tags = get_item_tags(workshop_item)
    item_type = get_item_type_from_tags(tags)
    rating = "N/A"
    comment_count = "N/A"
    if(item_type == "Level"):
        if(get_setting_value("ratings_levels") == 1):
            rating = get_item_rating(workshop_item)
        if(get_setting_value("comments_levels") == 1):
            comment_count = get_item_comment_count(workshop_item)
    if(item_type == "Model"):
        if(get_setting_value("ratings_models") == 1):
            rating = get_item_rating(workshop_item)
        if(get_setting_value("comments_models") == 1):
            comment_count = get_item_comment_count(workshop_item)
    creator_status = "N/A"
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

def get_creator_contribution_count(creator_id):
    driver.get(f"https://steamcommunity.com/profiles/{creator_id}/myworkshopfiles/?appid=477160")
    try:
        wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, 'workshopBrowsePagingInfo')) > 0)
    except TimeoutException:
        print("Could not find expected number of items.")
        return 0
    contribution_count_string = driver.find_element(By.CLASS_NAME, 'workshopBrowsePagingInfo').text
    contribution_count_string = int(contribution_count_string.split('of ')[1].split(' entries')[0].replace(',', ''))
    return contribution_count_string

def get_creator_followers_count(creator_id):
    if driver.current_url != f"https://steamcommunity.com/profiles/{creator_id}/myworkshopfiles/?appid=477160":
        driver.get(f"https://steamcommunity.com/profiles/{creator_id}/myworkshopfiles/?appid=477160")
    try:
        wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, 'followStat')) > 0)
    except TimeoutException:
        print("Could not find expected number of followers.")
        return 0
    followers_count_string = driver.find_element(By.CLASS_NAME, 'followStat').text
    followers_count = int(followers_count_string.replace(',', ''))
    return followers_count

def get_item_creator_country(user):
    if('loccountrycode' in user['player']):
        return user['player']['loccountrycode']
    else:
        return "N/A"

def get_item_creator_language(user, workshop_item):
    other_asian_language_codes = ['id', 'ja', 'ko', 'th', 'tl', 'vi']
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
    #The same goes for other asian languages after the chinese override.
    if 'zh' not in detected_language:
        for string in strings:
            try:
                if 'zh' in detect(string):
                    return'zh-cn'
            except:
                continue
    elif detected_language not in other_asian_language_codes:
        for string in strings:
            try:
                if detect(string) in other_asian_language_codes:
                    return detect(string)
            except:
                continue
    return detected_language

def get_item_tus(workshop_item):
    return workshop_item['subscriptions']

def get_item_rating(workshop_item):
    file_id = workshop_item["publishedfileid"]
    item_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={file_id}"
    if driver.current_url != item_url:
        driver.get(item_url)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "workshopAdminStatsBarPercent")))
        rating = driver.find_element(By.CLASS_NAME, "workshopAdminStatsBarPercent").text
    except TimeoutException:
        rating = "N/A"
    return rating

def get_item_comment_count(workshop_item):
    file_id = workshop_item["publishedfileid"]
    item_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={file_id}"
    if driver.current_url != item_url:
        driver.get(item_url)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "comments")))
        comment_count = driver.find_element(By.CLASS_NAME, "comments").text.split('Comments')[1]
    except TimeoutException:
        comment_count = "N/A"
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

def get_top_100_appIDs_steamDB():
    driver.get("https://steamdb.info/charts/?category=30")
    wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'tr.app')) > 0)
    steamdbGames = driver.find_elements(By.CSS_SELECTOR, 'tr.app')
    listOfAppIDS = []
    for game in steamdbGames:
        appID = game.get_attribute('data-appid')
        listOfAppIDS.append(appID)
    return listOfAppIDS

def create_game_item(gameAppID):
    gameName = steam.apps.get_app_details(gameAppID)[gameAppID]['data']['name']
    gameWorkShopItemCount = get_game_workshop_count(gameAppID)
    newGame = Game(gameAppID, gameName, gameWorkShopItemCount)
    return newGame

def get_game_name(gameAppID):
    return steam.apps.get_app_details(gameAppID)[gameAppID]['data']['name']

def get_game_workshop_count(gameAppID):
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

def apply_setting_value(setting_name, setting_value):
    setting_file = open("settings.txt", "r")
    setting_lines = setting_file.readlines()
    setting_file.close()
    setting_file = open("settings.txt", "w")
    for line in setting_lines:
        if line.split(":")[0] == setting_name:
            line = f"{setting_name}:{setting_value}\n"
        setting_file.write(line)
    setting_file.close()

def get_setting_value(setting_name):
    setting_file = open("settings.txt", "r")
    setting_lines = setting_file.readlines()
    setting_file.close()
    for line in setting_lines:
        if line.split(":")[0] == setting_name:
            return int(line.split(":")[1])
    return None

def log_in_steam_user(user, password):
    #This function will take the user and password args, load the steam log in page and log in the user.
    #If the log in is succesful, the function will return 0
    #If there is a verification code screen shown, the program will return 1
    #If there is a "use steam mobile app to log in" screen shown, the program will return 2
    driver.get('https://steamcommunity.com/login/home')
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_2eKVn6g5Yysx9JmutQe7WV")))
    except TimeoutException:
        print("Could not find username input.")
        return
    username_input = driver.find_elements(By.CLASS_NAME, "_2eKVn6g5Yysx9JmutQe7WV")[0]
    password_input = driver.find_elements(By.CLASS_NAME, "_2eKVn6g5Yysx9JmutQe7WV")[1]
    username_input.send_keys(user)
    password_input.send_keys(password)
    submit_button = driver.find_element(By.CLASS_NAME, "_2QgFEj17t677s3x299PNJQ")
    submit_button.click()
    if check_steam_user_logged_in(driver):
        print("Logged in.")
        return 0
    elif len(driver.find_elements(By.CLASS_NAME, "HPSuAjHOkNfMHwURXTns7")) > 0:
        print("Verification code screen found.")
        return 1
    elif len(driver.find_elements(By.CLASS_NAME, "_7LmnTPGNvHEfRVizEiGEV")) > 0:
        print("Use steam mobile app to log in screen found.")
        return 2    

def verify_steam_user_log_in(verify_code):
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "HPSuAjHOkNfMHwURXTns7")))
    except TimeoutException:
        print("No verification screen found.")
    
    verification_inputs = driver.find_elements(By.CLASS_NAME, "HPSuAjHOkNfMHwURXTns7")
    for i in range(len(verify_code)):
        verification_inputs[i].send_keys(verify_code[i])

def check_steam_user_logged_in():
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "account_name")))
        time.sleep(2)
        account_name = driver.find_element(By.ID, "account_dropdown").get_attribute('innerHTML')
        account_name = account_name.split('<span class="account_name">')[1].split('</span>')[0]
        print(f"Logged in as {account_name}")
        print(bool(account_name))
        return account_name
    except TimeoutException:
        return False

def check_for_settings_file():
    if not os.path.exists("settings.txt"):
        setting_file = open("settings.txt", "w")
        setting_file.write("display_browser:0\n")
        setting_file.write("ratings_levels:0\n")
        setting_file.write("comments_levels:0\n")
        setting_file.write("ratings_models:0\n")
        setting_file.write("comments_models:0\n")
        setting_file.close()
def check_for_creator_status_file():
    if not os.path.exists("creator_status_contacted.txt"):
        creator_status_file = open("creator_status_contacted.txt", "w")
        creator_status_file.close()
    if not os.path.exists("creator_status_pending.txt"):
        creator_status_file = open("creator_status_pending.txt", "w")
        creator_status_file.close()
    if not os.path.exists("creator_status_signed.txt"):
        creator_status_file = open("creator_status_signed.txt", "w")
        creator_status_file.close()
