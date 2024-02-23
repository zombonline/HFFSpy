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

class Game:
    def __init__(self, appID, name, amountOfItems):
        self.appID = appID
        self.name = name
        self.amountOfItems = amountOfItems

def CreateGameObject(gameAppID):
    link = "https://steamcommunity.com/workshop/browse/?appid=" + gameAppID + "&browsesort=trend&section=readytouseitems"
    driver.get(link)
    try:
        wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopBrowsePagingInfo')) > 0)
        itemCountText = driver.find_element(By.CSS_SELECTOR, 'div.workshopBrowsePagingInfo').text
        gameWorkShopItemCount = itemCountText.split('of ')[1].split(' entries')[0].replace(',', '')
        gameName = driver.title
    except TimeoutException:

        print()
        print()
        print()
        print("Error finding number of items for '" + gameAppID + "'")
        print("Double check the appID and try again")
        print("If the appID is correct, the issue may be network related") 
        gameWorkShopItemCount = "Error"
        gameName = "Error"

    newGame = Game(gameAppID, gameName, gameWorkShopItemCount)
    return newGame

def WriteToExcel():
    year = date.today().year
    month = date.today().strftime('%b')

    workbook = xlsxwriter.Workbook('UGCOfMajorGames ' + month + ' ' + str(year) + '.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'AppID')
    worksheet.write('B1', 'Game Name')
    worksheet.write('C1', 'Amount of Items')
    worksheet.write('C2', month + ' ' + str(year))
    row = 2
    for i in games:
        worksheet.write(row, 0, i.appID)
        worksheet.write(row, 1, i.name)
        worksheet.write(row, 2, i.amountOfItems)
        row += 1
    workbook.close()
    print("Path to Excel file: " + os.path.abspath('UGCOfMajorGames ' + month + ' ' + str(year) + '.xlsx'))

def ProgressBar(progress, total):
    percent = (progress/float(total)) * 100
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")
    if(progress == total):
        print("\n")

print("UGCOfMajorGames Scanner v1.0\n\n")

#region Selenium Setup
options = Options()
options.add_argument("--headless")
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


try:
    appIDFile = open('ListOfAppIDs.txt', 'r')
except FileNotFoundError:
    print("ListOfAppIDs.txt not found. Creating file...")
    appIDFile = open('ListOfAppIDs.txt', 'w')
    appIDFile = open('ListOfAppIDs.txt', 'r')
#print path to listofappids.txt
print("Edit ListOfAppIDs.txt to add appIDs to scan")
print("Path to ListOfAppIDs.txt: " + os.path.abspath('ListOfAppIDs.txt') +" \n\n")
for line in appIDFile:
    listOfAppIDS.append(line.split(" ")[0])
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
