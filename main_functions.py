import time
from langdetect import detect
from steam import Steam
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

#WORKSHOP ITEM FUNCTIONS
class WorkshopItem:
    def __init__(self, title, creator_id, creator_name, country, language, tus, rating, comment_count, date_posted, tags, item_type, creator_status, contribution_count, followers, visitors, item_id):
        self.title = title
        self.creator_id = creator_id
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
        self.contribution_count = contribution_count
        self.followers = followers
        self.visitors = visitors
        self.item_id = item_id

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
    if 'entries' in total_items_string:
        #Showing 1-30 of 5,187 entries
        total_items = int(total_items_string.split('of ')[1].split(' entries')[0].replace(',', ''))
    elif '项条目' in total_items_string:
        #正在显示第 1 - 30 项，共 7,219 项条目
        total_items = int(total_items_string.split('共 ')[1].split(' 项条目')[0].replace(',', ''))
    return total_items

def get_item_ids(amount = None):
    if amount is None:
        amount = get_total_items()
    item_ids = []
    maxItemsFound = False
    while len(item_ids) < amount and maxItemsFound == False:
        try:
            wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem')) > 0)
        except:
            print("No items on page.")
        for item_css_element in driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem'):
            item_id = item_css_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('data-publishedfileid')
            item_ids.append(item_id)
        workshop_next_page()
        maxItemsFound = len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem')) == 0
    return item_ids[:amount]

def get_item_and_user_data(item_id):
    params = {
            'key': KEY,
            'itemcount': 1,
            'publishedfileids[0]': item_id
        }
    response = requests.post(url, data=params)
    if response.text:
        data = response.json()
    else:
        print(f"No data received for item_id: {item_id}")
        return None, None
    data = response.json()
    if 'creator' in data['response']['publishedfiledetails'][0]:
        workShopItem = data['response']['publishedfiledetails'][0]
        user = steam.users.get_user_details(data['response']['publishedfiledetails'][0]['creator'])
        return workShopItem, user
    else:
        print(f"Item ID {item_id} has no creator data.")
        return None, None

def create_workshop_item(item_id, excel_outputs):
    workshop_item, user = get_item_and_user_data(item_id)
    if workshop_item is None or user is None:
        return WorkshopItem(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, item_id)
    title = get_item_title(workshop_item)
    creator_id = get_item_creator_id(workshop_item)
    creator_name = get_creator_name(user)
    country = get_creator_country(user)
    detected_language = get_creator_language(user, workshop_item)
    tus = get_item_tus(workshop_item)
    date_posted = get_item_date_posted(workshop_item)
    tags = get_item_tags(workshop_item)
    item_type = get_item_type_from_tags(tags)
    creator_status = get_creator_status(creator_id)
    contribution_count = "N/A"
    followers = "N/A"
    visitors = "N/A"
    rating = "N/A"
    comment_count = "N/A"
    
    #These properties require further scraping and slow the scan down, they are optional.

    # These three are scraped from the same page, they're banded together for this reason.
    if excel_outputs['Rating'][1]:
        rating = get_item_rating(workshop_item)
    if excel_outputs['Comment Count'][1]:
        comment_count = get_item_comment_count(workshop_item)
    if excel_outputs['Visitors'][1]:
        visitors = get_item_visitors(workshop_item)
    # These two are scraped from the same page, they're banded together for this reason.
    if excel_outputs['Contribution Count'][1]:
        contribution_count = get_creator_contribution_count(workshop_item['creator'])
    if excel_outputs['Followers'][1]:
        followers = get_creator_followers_count(workshop_item['creator'])

    return WorkshopItem(title, creator_id, creator_name, country, detected_language, tus, rating, comment_count, date_posted, tags, item_type, creator_status, contribution_count, followers, visitors, item_id)

def get_item_title(workshop_item):
    return workshop_item['title']

def get_item_creator_id(workshop_item):
    return workshop_item['creator']

def get_user_details(creator_id):
    try:
        return steam.users.get_user_details(creator_id)
    except:
        return None

def get_creator_name(user):
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
        return "N/A"
    contribution_count = driver.find_element(By.CLASS_NAME, 'workshopBrowsePagingInfo').text
    if 'entries' in contribution_count:
        #Showing 1-2 of 2 entries
        contribution_count = int(contribution_count.split('of ')[1].split(' entries')[0].replace(',', ''))
    elif '项条目' in contribution_count:
        #正在显示第 1 - 2 项，共 2 项条目
        contribution_count = int(contribution_count.split('共 ')[1].split(' 项条目')[0].replace(',', ''))
    return contribution_count

def get_creator_followers_count(creator_id):
    if driver.current_url != f"https://steamcommunity.com/profiles/{creator_id}/myworkshopfiles/?appid=477160":
        driver.get(f"https://steamcommunity.com/profiles/{creator_id}/myworkshopfiles/?appid=477160")
    try:
        wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, 'followStat')) > 0)
    except TimeoutException:
        print("Could not find expected number of followers.")
        return "N/A"
    followers_count_string = driver.find_element(By.CLASS_NAME, 'followStat').text
    followers_count = int(followers_count_string.replace(',', ''))
    return followers_count

def get_creator_status(creator_id):
    if creator_id in signed_users:
        return "Signed"
    elif creator_id in contacted_users:
        return "Contacted"
    elif creator_id in planned_users:
        return "Pending"
    else:
        return None

def get_creator_country(user):
    if('loccountrycode' in user['player']):
        return user['player']['loccountrycode']
    else:
        return "N/A"
    
def get_creator_language(user, workshop_item):
    other_asian_language_codes = ['id', 'ja', 'ko', 'th', 'tl', 'vi']
    #chinese override, if the user's country is already display as China, then the language is Chinese
    if(get_creator_country(user) == 'CN'):
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
        rating = driver.find_element(By.CLASS_NAME, "workshopAdminStatsBarPercent").text.split('%')[0]+"%"
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
        comment_count = driver.find_element(By.CLASS_NAME, "comments").text
        if 'Comments' in comment_count:
            #0 Comments
            comment_count = comment_count.split('Comments')[0].replace('留言', '')
        elif '条留言' in comment_count:
            #0 条留言
            comment_count = comment_count.split('条留言')[0]
    except TimeoutException:
        comment_count = "N/A"
    return comment_count

def get_item_visitors(workshop_item):
    file_id = workshop_item["publishedfileid"]
    item_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={file_id}"
    if driver.current_url != item_url:
        driver.get(item_url)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "stats_table")))
        stats_table = driver.find_element(By.CLASS_NAME, "stats_table")
        tbody = stats_table.find_element(By.TAG_NAME, "tbody")
        first_row = tbody.find_element(By.TAG_NAME, "tr")
        visitors = first_row.text.split(' ')[0].replace(',', '')
    except TimeoutException:
        visitors = "N/A"
    return visitors

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

#STEAM GAME FUNCTIONS
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
    try:
        gameWorkShopItemCount = get_total_items()
    except TimeoutException:
        print("Timed out waiting for page to load")
        return
    return gameWorkShopItemCount

#EXTRA FUNCTIONS
def apply_setting_value(setting_name, setting_value):
    #open settings file from appdata
    appdata_dir = get_appdata_dir()
    setting_file = open(appdata_dir + "\\settings.txt", "r")
    setting_lines = setting_file.readlines()
    setting_file.close()
    setting_file = open(appdata_dir + "\\settings.txt", "w")
    for line in setting_lines:
        if line.split(":")[0] == setting_name:
            line = f"{setting_name}:{setting_value}\n"
        setting_file.write(line)
    setting_file.close()

def get_setting_value(setting_name, return_type = "int"):
    appdata_dir = get_appdata_dir()
    setting_file = open(appdata_dir + "\\settings.txt", "r")
    setting_lines = setting_file.readlines()
    setting_file.close()
    for line in setting_lines:
        if line.split(":")[0] == setting_name:
            if return_type == "int":
                return int(line.split(":")[1])
            elif return_type == "str":
                return line.split(":")[1].strip()
    return None

def log_in_steam_user(user, password, thread_return_queue=None):
    #This function will take the user and password args, load the steam log in page and log in the user.
    #If the log in is succesful, the function will return 0
    #If there is a verification code screen shown, the program will return 1
    #If there is a "use steam mobile app to log in" screen shown, the program will return 2
    driver.get('https://steamcommunity.com/login/home')
    if(check_steam_user_logged_in()):
        return 0
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_2GBWeup5cttgbTw8FM3tfx")))
    except TimeoutException:
        print("Could not find username input.")
        return None
    #find the first text input. This is the username input
    username_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
    username_input.send_keys(user)
    password_input.send_keys(password)
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit_button.click()
    if check_steam_user_logged_in():
        return_value = 1
    elif len(driver.find_elements(By.CLASS_NAME, "HPSuAjHOkNfMHwURXTns7")) > 0:
        return_value = 2
    elif (driver.find_element(By.XPATH, "//img[@src='https://community.akamai.steamstatic.com/public/images/applications/community/login_mobile_auth.png?v=e2f09e9d649508c82f214f84aba44363']")):
        return_value = 3
    elif len(driver.find_elements(By.CLASS_NAME, "A3Y-u39xir9DKtvLEOcnd")) > 0:
        return_value = 4
    if thread_return_queue is not None:
        thread_return_queue.put(return_value)
    else:
        return return_value

def verify_steam_user_log_in(verify_code):
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "HPSuAjHOkNfMHwURXTns7")))
    except TimeoutException:
        print("No verification screen found.")
    verification_inputs = driver.find_elements(By.CLASS_NAME, "HPSuAjHOkNfMHwURXTns7")
    for i in range(len(verify_code)):
        verification_inputs[i].send_keys(verify_code[i])
    if check_steam_user_logged_in():
        return True
    else:
        for i in range(len(verification_inputs)):
            verification_inputs[i].clear()
        return False

def check_steam_user_logged_in():
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "account_name")))
        account_name = driver.find_element(By.ID, "account_dropdown").get_attribute('innerHTML')
        account_name = account_name.split('<span class="account_name">')[1].split('</span>')[0]
        return account_name
    except TimeoutException:
        return False

def check_for_settings_file():
    try:
        appdata_dir = get_appdata_dir()
        if not os.path.exists(appdata_dir + "\\settings.txt"):
            settings_file = open(appdata_dir + "\\settings.txt", "w")
            settings_file.write("display_browser:1\n")
            settings_file.write("steam_api_key:\n")
            settings_file.close()
    except:
        return False

def check_for_creator_status_files():
    try:
        appdata_dir = get_appdata_dir()
        if not os.path.exists(appdata_dir + "\\creator_status_signed.txt"):
            signed_file = open(appdata_dir + "\\creator_status_signed.txt", "w")
            signed_file.close()
        if not os.path.exists(appdata_dir + "\\creator_status_contacted.txt"):
            contacted_file = open(appdata_dir + "\\creator_status_contacted.txt", "w")
            contacted_file.close()
        if not os.path.exists(appdata_dir + "\\creator_status_planned.txt"):
            planned_file = open(appdata_dir + "\\creator_status_planned.txt", "w")
            planned_file.close()
        return True
    except:
        return False

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
    else:
        print("Browser will be displayed")
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    chrome_driver_path = os.path.join(base_dir, "chromedriver.exe")
    print(f"Looking for ChromeDriver at {chrome_driver_path}")
    if not os.path.exists(chrome_driver_path):
        print("ChromeDriver not found. Please download the latest version of ChromeDriver from https://sites.google.com/chromium.org/driver/ and place it in the same directory as this script.")
        return False
    else:
        print("ChromeDriver found.")
    webdriver_service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=webdriver_service, options=options)
    wait = WebDriverWait(driver, 10)
    return driver

def set_steam_api_key():
    global KEY, steam, url
    KEY = get_setting_value("steam_api_key", "str")
    steam = Steam(KEY)
    url = f"https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    try:
        response = get_item_and_user_data(3256120107)
        if 'error' in response:
            print("Invalid Steam API key. Please enter a valid key in the settings file.")
            return False
    except:
        print("An error occurred while testing the Steam API key.")
        return False
    return True

def populate_user_lists():
    global signed_users, contacted_users, planned_users
    signed_users = []
    contacted_users = []
    planned_users = []
    appdata_dir = get_appdata_dir()
    appdata_dir = get_appdata_dir()
    with open(appdata_dir + "\\creator_status_signed.txt", "r") as creator_status_file:    
        signed_users = [int(line[line.rfind("(")+1: -2].strip()) for line in creator_status_file.readlines()]
    with open(appdata_dir + "\\creator_status_contacted.txt", "r") as creator_status_file:
        contacted_users = [int(line[line.rfind("(")+1: -2].strip()) for line in creator_status_file.readlines()]
    with open(appdata_dir + "\\creator_status_planned.txt", "r") as creator_status_file:
        planned_users = [int(line[line.rfind("(")+1: -2].strip()) for line in creator_status_file.readlines()]

def get_appdata_dir():
    appdata_dir = os.getenv('APPDATA')
    if not os.path.exists(appdata_dir + "\\HFFSpy"):
        os.makedirs(appdata_dir + "\\HFFSpy")
    return appdata_dir + "\\HFFSpy"


KEY = None
steam = None
url = None 
driver = None
wait = None
signed_users = []
contacted_users = []
planned_users = []