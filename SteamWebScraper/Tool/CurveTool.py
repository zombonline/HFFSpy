import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry
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
from datetime import datetime, timedelta
from langdetect import detect
import xlsxwriter
import math
from decouple import config
from enum import Enum

import TopUGC
import TotalUGC
import threading
app = tk.Tk()
app.title("Curve Tool")
app.geometry("800x600")

# Create the main frame
main_frame = ctk.CTkFrame(app)
main_frame.pack(expand=True, fill="both")

def set_up_home_page():
    # Create the home frame
    home_frame = ctk.CTkFrame(main_frame)
    home_frame.pack(expand=True, fill="both")
    # Create the home canvas
    home_canvas = ctk.CTkCanvas(home_frame)
    home_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(home_canvas, text="Home", text_color='black', font=("Arial", 24))
    title_label.pack()
    #Create the 'Download Chromdriver here' button
    download_chromedriver_button = ctk.CTkButton(home_canvas, text="Download Chromedriver here", command=lambda: os.system("start https://googlechromelabs.github.io/chrome-for-testing/"))
    download_chromedriver_button.pack()
    #Navigation Buttons
    total_UGC_count_button = ctk.CTkButton(home_canvas, text="Total UGC Count", command=lambda: load_page("Total UGC Count"))   
    total_UGC_count_button.pack()
    total_chinese_count_button = ctk.CTkButton(home_canvas, text="Total Chinese Count", command=lambda: load_page("Total Chinese Count"))
    total_chinese_count_button.pack()
    top_ugc_of_workshop_month_button = ctk.CTkButton(home_canvas, text="Top UGC of Workshop Month", command=lambda: load_page("Top Monthly Workshop Items"))
    top_ugc_of_workshop_month_button.pack()
def set_up_total_UGC_count_page():
    # Create the total UGC count frame
    total_UGC_count_frame = ctk.CTkFrame(main_frame)
    total_UGC_count_frame.pack(expand=True, fill="both")
    # Create the total UGC count canvas
    total_UGC_count_canvas = ctk.CTkCanvas(total_UGC_count_frame)
    total_UGC_count_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(total_UGC_count_canvas, text="Total UGC Count", text_color='black', font=("Arial", 24))
    title_label.pack()
    # Create the back button
    back_button = ctk.CTkButton(total_UGC_count_canvas, text="Back", command=lambda: load_page("Home"))
    back_button.pack()
    # Create the scan total UGC count button
    scan_total_UGC_count_button = ctk.CTkButton(total_UGC_count_canvas, text="Scan Total UGC Count", command=lambda: scan_total_UGC_count_button_click())
    scan_total_UGC_count_button.pack()
def set_up_scanning_page():
    # Create the loading frame
    loading_frame = ctk.CTkFrame(main_frame)
    loading_frame.pack(expand=True, fill="both")
    # Create the loading canvas
    loading_canvas = ctk.CTkCanvas(loading_frame)
    loading_canvas.pack(expand=True, fill="both")
    # Create the loading label
    loading_label = ctk.CTkLabel(loading_canvas, text="Scanning...", text_color='black', font=("Arial", 24))
    loading_label.pack()
def set_up_total_chinese_count_page():
    # Create the total Chinese count frame
    total_chinese_count_frame = ctk.CTkFrame(main_frame)
    total_chinese_count_frame.pack(expand=True, fill="both")
    # Create the total Chinese count canvas
    total_chinese_count_canvas = ctk.CTkCanvas(total_chinese_count_frame)
    total_chinese_count_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(total_chinese_count_canvas, text="Total Chinese Count", text_color='black', font=("Arial", 24))
    title_label.pack(pady=10)
    # Create the back button
    back_button = ctk.CTkButton(total_chinese_count_canvas, text="Back", command=lambda: load_page("Home"))
    back_button.pack()    
    # Create the date range frame
    date_range_frame = ctk.CTkFrame(total_chinese_count_canvas)
    date_range_frame.pack()
    # Create the date range start input
    date_range_start_label = ctk.CTkLabel(date_range_frame, text="Date Range Start", text_color='black')
    date_range_start_label.grid(row=0, column=0, padx=10)
    date_range_start = DateEntry(date_range_frame, textvariable=date_range_start_input, date_pattern="yyyy-mm-dd")
    date_range_start.grid(row=1, column=0, padx=10, pady=10)
    # Create the date range end input
    date_range_end_label = ctk.CTkLabel(date_range_frame, text="Date Range End", text_color='black')
    date_range_end_label.grid(row=0, column=1, padx=10)
    date_range_end = DateEntry(date_range_frame, textvariable=date_range_end_input, date_pattern="yyyy-mm-dd")
    date_range_end.grid(row=1, column=1, padx=10, pady=10)
    # Create the 'submit date range' button
    submit_date_range_button = ctk.CTkButton(date_range_frame, text="Submit Date Range", command=lambda: chinese_count_date_button_click(checkbox_frame))
    submit_date_range_button.grid(row=2, column=0, columnspan=2, pady=10)
    # Create the list of tags frame
    checkbox_frame = ctk.CTkFrame(total_chinese_count_canvas)
    checkbox_frame.pack()
    #Create the 'submit tags' button
    submit_tags_button = ctk.CTkButton(total_chinese_count_canvas, text="Submit Tags", command=lambda: chinese_count_submit_tags_button_click())
    submit_tags_button.pack()
    # Create the 'scrape page' button
    scrape_page_button = ctk.CTkButton(total_chinese_count_canvas, text="Scrape Page", command=lambda: chinese_count_scrape_page_button_click())
    scrape_page_button.pack()
def set_up_top_ugc_of_workshop_month_page():
    # Create the top monthly workshop items frame
    top_monthly_workshop_items_frame = ctk.CTkFrame(main_frame)
    top_monthly_workshop_items_frame.pack(expand=True, fill="both")
    # Create the top monthly workshop items canvas
    top_monthly_workshop_items_canvas = ctk.CTkCanvas(top_monthly_workshop_items_frame)
    top_monthly_workshop_items_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(top_monthly_workshop_items_canvas, text="Top Monthly Workshop Items", text_color='black', font=("Arial", 24))
    title_label.pack()
    # Create the back button
    back_button = ctk.CTkButton(top_monthly_workshop_items_canvas, text="Back", command=lambda: load_page("Home"))
    back_button.pack()
    # Create the date range frame
    date_range_frame = ctk.CTkFrame(top_monthly_workshop_items_canvas)
    date_range_frame.pack()
    # Create the date range start input
    date_range_start_label = ctk.CTkLabel(date_range_frame, text="Date Range Start", text_color='black')
    date_range_start_label.grid(row=0, column=0, padx=10)
    date_range_start = DateEntry(date_range_frame, textvariable=date_range_start_input, date_pattern="yyyy-mm-dd")
    date_range_start.grid(row=1, column=0, padx=10, pady=10)
    # Create the date range end input
    date_range_end_label = ctk.CTkLabel(date_range_frame, text="Date Range End", text_color='black')
    date_range_end_label.grid(row=0, column=1, padx=10)
    date_range_end = DateEntry(date_range_frame, textvariable=date_range_end_input, date_pattern="yyyy-mm-dd")
    date_range_end.grid(row=1, column=1, padx=10, pady=10)
    # Create the amount of items to grab input
    amount_of_items_label = ctk.CTkLabel(date_range_frame, text="Amount of Items to Grab", text_color='black')
    amount_of_items_label.grid(row=3, column=0, padx=10)
    amount_of_items_input = ctk.CTkEntry(date_range_frame)
    amount_of_items_input.grid(row=4, column=0, padx=10, pady=10)
    # Create the scan top ugc of workshop month button
    scan_top_ugc_of_workshop_month_button = ctk.CTkButton(top_monthly_workshop_items_canvas, text="Scan Top UGC of Workshop Month", command=lambda: scan_top_ugc_of_workshop_month_click(date_range_start_input.get(), date_range_end_input.get(), amount_of_items_input.get()))
    scan_top_ugc_of_workshop_month_button.pack()

   

def load_page(page):
    for widget in main_frame.winfo_children():
        widget.destroy()
    if page == "Home":
        set_up_home_page()
    elif page == "Total UGC Count":
        set_up_total_UGC_count_page()
    elif page == "Total Chinese Count":
        set_up_total_chinese_count_page()
    elif page == "Top Monthly Workshop Items":
        set_up_top_ugc_of_workshop_month_page()
    elif page == "Scanning":
        set_up_scanning_page()
    else:
        print("Error: Page not found")
        return
    global current_page
    current_page = page


#region input elements
date_range_start_input = tk.StringVar()
date_range_end_input = tk.StringVar()
tags_checklist_vars = {}
#endregion
#region tkinter functions
def scan_total_UGC_count_button_click():
    previous_page = current_page
    load_page("Scanning")
    
    def scan_and_load_previous():
        TotalUGC.scan_for_total_UGC_count(driver, wait)
        load_page(previous_page)
    threading.Thread(target=scan_and_load_previous).start()
def scan_top_ugc_of_workshop_month_click(start_date, end_date, amount_of_items):
    previous_page = current_page
    load_page("Scanning")
    
    def scan_and_load_previous():
        TopUGC.scan(driver, wait, start_date, end_date, amount_of_items)
        load_page(previous_page)
    threading.Thread(target=scan_and_load_previous).start()

def get_selected_list_element_index(list):
    selected_indices = list.curselection()
    if selected_indices:  
        first_selected_index = selected_indices[0]
        print(first_selected_index)
        return first_selected_index
    else:
        return None
def create_checklist(options, canvas):
    vars = {}
    for i in range(len(options)):
        var = tk.IntVar()
        vars[options[i]] = var
        options[i] = tk.Checkbutton(canvas, text=options[i], variable=var, onvalue=1, offvalue=0)
        options[i].grid(column=i//7, row=i%7)
    return vars
def chinese_count_date_button_click(canvas):
    submit_date_range_to_url(date_range_start_input.get(), date_range_end_input.get())
    global tags_checklist_vars
    tags_checklist_vars = create_checklist(load_tags_from_webpage(), canvas)
def chinese_count_submit_tags_button_click():
    apply_tags_to_url()
def chinese_count_scrape_page_button_click():
    workshop_item_ids = get_workshop_item_ids()
    workshopItems = create_workshop_item_objects_array(workshop_item_ids)
    print('items found: ' + str(len(workshopItems)))
    create_chinese_count_excel_sheet(workshopItems, datetime.strptime(date_range_start_input.get(), "%Y-%m-%d"), datetime.strptime(date_range_end_input.get(), "%Y-%m-%d"))
#endregion
def submit_date_range_to_url(start, end):
    start_timestamp = int(datetime.strptime(start, "%Y-%m-%d").timestamp())
    end_timestamp = int(datetime.strptime(end, "%Y-%m-%d").timestamp())
    link = f'https://steamcommunity.com/workshop/browse/?appid=477160&searchtext=&childpublishedfileid=0&browsesort=trend&section=readytouseitems&created_date_range_filter_start={start_timestamp}&created_date_range_filter_end={end_timestamp}&updated_date_range_filter_start=NaN&updated_date_range_filter_end=NaN'
    driver.get(link)
def load_chrome_driver():
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
    return driver
def load_tags_from_webpage():
    tags = []
    try:
        tag_elements = driver.find_elements(By.CLASS_NAME, "filterOption")
        for element in tag_elements:
            tags.append(element.text)
    except Exception as e:
        print(f"Error: {e}")
    return tags
def apply_tags_to_url():
    for key in tags_checklist_vars:
        wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, "filterOption")) > 0)
        for option in driver.find_elements(By.CLASS_NAME, "filterOption"):
            if key not in option.text:
                continue
            checkbox = option.find_element(By.TAG_NAME, "input")
            if checkbox.get_attribute("type") != "checkbox":
                continue

            if tags_checklist_vars[key].get() == 1:
                if not checkbox.get_attribute("checked"):
                    checkbox.click()
            elif tags_checklist_vars[key].get() == 0:
                if checkbox.get_attribute("checked"):
                    checkbox.click()
            break
def get_workshop_item_ids():
    targetText = driver.find_element(By.CSS_SELECTOR, 'div.workshopBrowsePagingInfo').text
    target = int(targetText.split('of ')[1].split(' entries')[0])
    print(f"Target: {target}")
    workshop_item_ids = []
    while len(workshop_item_ids) < target:
        try:
            wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem')) > 0)
        except TimeoutException:
            print("Timed out waiting for page to load")
            return []
        for element in driver.find_elements(By.CSS_SELECTOR, 'div.workshopItem'):
            element_id = element.find_element(By.CSS_SELECTOR, 'a').get_attribute('data-publishedfileid')
            workshop_item_ids.append(element_id)
            print(f"Added {element_id}")
        current_url = driver.current_url
        driver.get(current_url + "&p=" + str(math.ceil((len(workshop_item_ids)/30)+1)))
    return workshop_item_ids
def get_data_from_workshop_id(item_id):
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
def create_workshop_item_objects_array(workshop_item_ids):
    workshopItems = []
    for workshop_item_ids in workshop_item_ids:
        workshop_item, user = get_data_from_workshop_id(workshop_item_ids)
        #Get Title of workshop item
        title = workshop_item['title']
        #Get AuthorID of workshop item
        creator_id = workshop_item['creator']
        #Get Author Name of workshop item
        creator_name = user['player']['personaname']
        #Get Country of Author
        country = get_user_country(user)
        #Get language of workshop item
        detected_language = get_language_from_user_and_item(user, workshop_item)
        #Get date posted of workshop item
        date_posted = datetime.fromtimestamp(workshop_item['time_created'])
        #Get tags of workshop item
        tags = get_tags(workshop_item['tags'])
        #Get type of workshop item ("Model" or "Level")
        item_type = get_item_type_from_tags(tags)
        #create a new workshop item object and append it to list.
        workshopItems.append(WorkshopItem(title, creator_id, creator_name, country, detected_language, date_posted, tags, item_type))
    return workshopItems
def create_chinese_count_excel_sheet(workshop_data, start_date, end_date):
    workbook = xlsxwriter.Workbook(f'UGCChineseSpeakingCount_Week_{start_date.strftime("%m-%d-%Y")}_to_{end_date.strftime("%m-%d-%Y")}.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Date Posted')
    worksheet.write('B1', 'Title')
    worksheet.write('C1', 'Creator Name')
    worksheet.write('D1', 'Type')
    worksheet.write('E1', 'Country')
    worksheet.write('F1', 'Language')

    chineseLevels = 0
    chineseModels = 0
    totalLevels = 0
    totalModels = 0
    for(i, item) in enumerate(workshop_data):
        worksheet.write(i+1, 0, item.date_posted.strftime("%d-%m-%Y"))
        worksheet.write(i+1, 1, item.title)
        worksheet.write(i+1, 2, item.creator_name)
        worksheet.write(i+1, 3, item.item_type)
        worksheet.write(i+1, 4, item.country)
        worksheet.write(i+1, 5, item.detected_language)
        if item.detected_language == 'zh-cn':
            if item.item_type == 'Level':
                chineseLevels += 1
            elif item.item_type == 'Model':
                chineseModels += 1
        if item.item_type == 'Level':
            totalLevels += 1
        elif item.item_type == 'Model':
            totalModels += 1
    worksheet.write('H2', 'Models')
    worksheet.write('H3', 'Total Entries')
    worksheet.write('H4', 'Chinese Entries')
    worksheet.write('H5', 'Chinese Proportion')

    worksheet.write('H7', 'Levels')
    worksheet.write('H8', 'Total Entries')
    worksheet.write('H9', 'Chinese Entries')
    worksheet.write('H10', 'Chinese Proportion')

    worksheet.write('H12', 'Total')
    worksheet.write('H13', 'Total Entries')
    worksheet.write('H14', 'Chinese Entries')
    worksheet.write('H15', 'Chinese Proportion')

    worksheet.write('I3', totalModels)
    worksheet.write('I4', chineseModels)
    worksheet.write('I5', f"{chineseModels/totalModels:.2%}")

    worksheet.write('I8', totalLevels)
    worksheet.write('I9', chineseLevels)
    worksheet.write('I10', f"{chineseLevels/totalLevels:.2%}")

    worksheet.write('I13', totalLevels + totalModels)
    worksheet.write('I14', chineseLevels + chineseModels)
    worksheet.write('I15', f"{(chineseLevels + chineseModels)/(totalLevels + totalModels):.2%}")


    workbook.close()
    print("Excel sheet created")
def get_user_country(user):
    if('loccountrycode' in user['player']):
        return user['player']['loccountrycode']
    else:
        return "N/A"
def get_language_from_user_and_item(user, workshop_item):
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
def get_tags(tags):
    tag_strings = [tag['tag'] for tag in tags]
    tag_string = ', '.join(tag_strings)
    return tag_string
def get_item_type_from_tags(tags):
    if('Model' in tags):
        return "Model"
    elif('Levels' in tags):
        return "Level"
    elif('Lobbies' in tags):
        return "Lobby"
    else:
        return "N/A"
class WorkshopItem:
    def __init__(self, title, creator_ID, creator_name, country, detected_language, date_posted, tags, item_type):
        self.title = title
        self.creator_ID = creator_ID
        self.creator_name = creator_name
        self.detected_language = detected_language
        self.country = country
        self.date_posted = date_posted
        self.tags = tags
        self.item_type = item_type
KEY = config('STEAM_API_KEY')
steam = Steam(KEY)
url = f"https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"   
current_page = "Home"
load_page(current_page)
driver = load_chrome_driver()
wait = WebDriverWait(driver, 10)
app.mainloop()


