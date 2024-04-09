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

import data_functions


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
driver = None
wait = None

def get_top_100_games_via_steamDB():
    driver.get("https://steamdb.info/charts/?category=30")
    wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'tr.app')) > 0)
    steamdbGames = driver.find_elements(By.CSS_SELECTOR, 'tr.app')
    listOfAppIDS = []
    for game in steamdbGames:
        appID = game.get_attribute('data-appid')
        listOfAppIDS.append(appID)
    return listOfAppIDS

def create_game_items(listOfAppIDS):
    games = []
    for appID in listOfAppIDS:
        game = data_functions.create_game_item(appID, driver)
        games.append(game)
    return games

def scan_for_total_UGC_count(d):
    global driver
    driver = d
    global wait
    wait = WebDriverWait(driver, 10)

    games = create_game_items(get_top_100_games_via_steamDB())  

    WriteToExcel(games)
    print("Finished")
    #print path to excel file



