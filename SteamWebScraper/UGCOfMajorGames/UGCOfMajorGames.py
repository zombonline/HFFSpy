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
from datetime import date
import xlsxwriter
from steam import Steam
from decouple import config

class Game:
    def __init__(self, appID, name, amountOfItems):
        self.appID = appID
        self.name = name
        self.amountOfItems = amountOfItems

def CreateGameObject(gameAppID):
    link = "https://steamcommunity.com/workshop/browse/?appid=" + gameAppID
    driver.get(link)
    gameName = steam.apps.get_app_details(gameAppID)[gameAppID]['data']['name']
    gameWorkShopItemCount = "N/A"
    if gameAppID in driver.current_url:
        try:
            wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopBrowsePagingInfo')) > 0)
            itemCountText = driver.find_element(By.CSS_SELECTOR, 'div.workshopBrowsePagingInfo').text
            gameWorkShopItemCount = int(itemCountText.split('of ')[1].split(' entries')[0].replace(',', ''))
        except TimeoutException:
            print("Timed out waiting for page to load")
            return

    newGame = Game(gameAppID, gameName, gameWorkShopItemCount)
    return newGame

def WriteToExcel():
    workbook = xlsxwriter.Workbook('UGCOfMajorGames.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Rank')
    worksheet.write('B1', 'Game Name')
    worksheet.write('C1', f'Amount of Workshop Items as of {date.today()}')

    for i in range(len(games)):
        worksheet.write(i+1, 0, i+1)
        worksheet.write(i+1, 1, games[i].name)
        worksheet.write(i+1, 2, games[i].amountOfItems)
    
    workbook.close()

def ProgressBar(progress, total):
    percent = (progress/float(total)) * 100
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")
    if(progress == total):
        print("\n")

print("UGCOfMajorGames Scanner v1.0\n\n")

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)


#region Selenium Setup
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
wait = WebDriverWait(driver, 5)
#endregion

listOfAppIDS = []
games = []


# try:
#     appIDFile = open('ListOfAppIDs.txt', 'r')
# except FileNotFoundError:
#     print("ListOfAppIDs.txt not found. Creating file...")
#     appIDFile = open('ListOfAppIDs.txt', 'w')
#     appIDFile = open('ListOfAppIDs.txt', 'r')
# #print path to listofappids.txt
# print("Edit ListOfAppIDs.txt to add appIDs to scan")
# print("Path to ListOfAppIDs.txt: " + os.path.abspath('ListOfAppIDs.txt') +" \n\n")

# for line in appIDFile:
#     listOfAppIDS.append(line.split(" ")[0])

#get top 100 games with workshop
driver.get("https://steamdb.info/charts/?category=30")
wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'tr.app')) > 0)
steamdbGames = driver.find_elements(By.CSS_SELECTOR, 'tr.app')
for game in steamdbGames:
    appID = game.get_attribute('data-appid')
    print(appID)
    listOfAppIDS.append(appID)
print("Scanning through " + str(len(listOfAppIDS)) + " appIDs...")
if(len(listOfAppIDS) > 0):
    ProgressBar(len(games), len(listOfAppIDS))  
    for i in listOfAppIDS:
        newGame = CreateGameObject(i)
        games.append(newGame)
        ProgressBar(len(games), len(listOfAppIDS))
else:
    driver.quit()
    print("ListOfAppIDs.txt is empty. Please add appIDs to scan")
    input("Press Enter to close the program...")
    sys.exit(1)

WriteToExcel()
driver.quit()
print("Finished")
#print path to excel file
input("Press Enter to close the program...")
