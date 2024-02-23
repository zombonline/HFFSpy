import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from datetime import date, timedelta
import xlsxwriter
from selenium.webdriver.common.keys import Keys

from concurrent.futures import ThreadPoolExecutor
from queue import Queue

class WorkshopItem:
    def __init__(self, title, author, country, date_posted, tags):
        self.title = title
        self.author = author
        self.country = country
        self.date_posted = date_posted
        self.tags = tags

        

def NextPage():
    currentPageUrl = driver.current_url
    currentPage = int(currentPageUrl.split('p=')[1])
    nextPage = currentPage + 1
    nextPageUrl = currentPageUrl.split('p=')[0] + 'p=' + str(nextPage)
    driver.get(nextPageUrl)
    # try:
    #     cookieWait.until(EC.visibility_of_element_located((By.ID, 'cookiePrefPopup')))
    #     driver.find_element(By.ID, 'acceptAllButton').click()
    # except TimeoutException:
    #     pass
    # buttons = driver.find_elements(By.CSS_SELECTOR, 'a.pagebtn')
    # wait.until(lambda driver: len(buttons) > 0)
    # if(len(buttons) == 1):
    #     buttons[0].click()
    # elif(len(buttons) == 2):
    #     buttons[1].click()
    # return

def ScrapePage():
    try:
        wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem')) > 0)
    except TimeoutException:
        print("Timed out waiting for page to load")
        return []
    workShopItems = driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem')
    return workShopItems

def ExtractWorkshopItemElementContent(listOfWorkshopItemElements):
    workshopItems = []

    # Define a function that will be run in each thread
    def process_workshop_item(workshopItemElement):
        title = workshopItemElement.find_element(By.CSS_SELECTOR, 'div.workshopItemTitle').text
        author = workshopItemElement.find_element(By.CSS_SELECTOR, 'div.workshopItemAuthorName').text.split(' ')[1]
        link = workshopItemElement.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        newDriver = browser_queue.get()
        newDriver.get(link)

        newWait = WebDriverWait(newDriver, 1)
        try:
            newWait.until(lambda newDriver: len(newDriver.find_elements(By.CSS_SELECTOR, 'div.detailsStatRight')) > 0)
            date_posted = FormatDate(newDriver.find_element(By.CSS_SELECTOR, 'div.detailsStatRight:nth-child(2)').text)
            tags = newDriver.find_element(By.CSS_SELECTOR, 'div.rightDetailsBlock').text
        except TimeoutException:
            date_posted = FormatDate('31 Dec @ 9:24pm')
            tags = 'None'

        
        #load the author's profile to get the country
        profileLink = newDriver.find_element(By.CSS_SELECTOR, 'div.friendBlock').find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        newDriver.get(profileLink)
        try:
            newWait.until(lambda newDriver: len(newDriver.find_elements(By.CSS_SELECTOR, 'div.header_real_name')) > 0)
            country = newDriver.find_element(By.CSS_SELECTOR, 'div.header_real_name').text
        except TimeoutException:
            country = 'Unknown'

        browser_queue.put(newDriver)


        return WorkshopItem(title, author, country, date_posted, tags)

    # Use a ThreadPoolExecutor to run the function in multiple threads
    with ThreadPoolExecutor(max_workers=5) as executor:
        workshopItems = list(executor.map(process_workshop_item, listOfWorkshopItemElements))

    return workshopItems

def FormatDate(dateString):
    #remove time
    dateString = dateString.split('@')[0]
    day = dateString.split(' ')[0].zfill(2)
    month = dateString.split(' ')[1]
    if(',' in month):
        month = month.split(',')[0]
    month = str(MonthToInt(month)).zfill(2)
    year = dateString.split(' ')[2]
    if year == '':
        year = str(date.today().year)
    
    dateObject = date(int(year), int(month), int(day))
    return(dateObject)

def MonthToInt(month):
    switcher = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    return switcher.get(month, None)

def ProgressBar(progress, total):
    percent = (progress/float(total)) * 100
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")
    if(progress == total):
        print("\n")



# Create a queue to hold the browser instances
browser_queue = Queue()

# Create a pool of browser instances
for _ in range(5):  # Adjust the size of the pool as needed
    newOptions = Options()
    # newOptions.add_argument("--headless")
    newOptions.add_argument("--disable-gpu")
    newOptions.add_argument("--window-size=1920,1080")
    newOptions.add_argument("--log-level=3")
    prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
    newOptions.add_experimental_option("prefs", prefs)
    newOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    newDriver = webdriver.Chrome(service=Service(r"C:\Users\megaz\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"), options=newOptions)
    browser_queue.put(newDriver)
  
content = []

appID = input("Enter the app ID: ")
link = "https://steamcommunity.com/workshop/browse/?appid=" + str(appID) + "&browsesort=mostrecent&section=readytouseitems&actualsort=mostrecent&p=1"
pages = int(input("How many pages would you like to scrape? "))


options = Options()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=Service(r"C:\Users\megaz\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"), options=options)
driver.get(link)
#check here if review page loads

wait = WebDriverWait(driver,60);
cookieWait = WebDriverWait(driver, 2)
startTime = time.time()
for i in range(0, pages):
    try:
        content = content + (ExtractWorkshopItemElementContent(ScrapePage()))
        ProgressBar(len(content), pages*30)
        NextPage()
    except TimeoutException:
        print("Page timed out. Moving to the next page.")
        continue
print(str(len(content)) + " items scraped.")
endTime = time.time()
print("Time taken: " + str(round(endTime - startTime)) + " seconds")

for i in range(0, 5):
    driver = browser_queue.get()
    driver.quit()

driver.quit()


# Write content to a notepad file.
with open('workshopItems.txt', 'w', encoding='utf-8') as file:
    for item in content:
        file.write("Title: " + item.title + '\n')
        file.write("Author: " + item.author + '\n')
        file.write("Country: " + item.country + '\n')
        file.write("Tags: " + item.tags + '\n')
        file.write("Date Posted: " + str(item.date_posted) + '\n\n')
