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

def CreateGameObject(gameAppID, driver, wait):
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

def WriteToExcel(games):
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


KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

def scan_for_total_UGC_count(driver, wait):
    listOfAppIDS = []
    games = []

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
        for i in listOfAppIDS:
            newGame = CreateGameObject(i, driver, wait)
            games.append(newGame)

    WriteToExcel(games)
    print("Finished")
    #print path to excel file



