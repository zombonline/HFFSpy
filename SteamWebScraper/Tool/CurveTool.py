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
import chinese_count
import data_functions
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
    settings_button = ctk.CTkButton(home_canvas, text="Settings", command=lambda: load_page("Settings"))
    settings_button.pack()
    creator_button = ctk.CTkButton(home_canvas, text="Creator", command=lambda: load_page("Creator"))
    creator_button.pack()
    steam_login_button = ctk.CTkButton(home_canvas, text="Steam Login", command=lambda: load_page("Steam Login"))
    steam_login_button.pack()
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
    # Create the 'scrape page' button
    scrape_page_button = ctk.CTkButton(total_chinese_count_canvas, text="Scan", command=lambda: scan_total_chinese_count_button_click(date_range_start_input.get(), date_range_end_input.get()))
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
    scan_top_ugc_of_workshop_month_button = ctk.CTkButton(top_monthly_workshop_items_canvas, text="Scan Top UGC of Workshop Month", command=lambda: scan_top_ugc_of_workshop_month_button_click(date_range_start_input.get(), date_range_end_input.get(), int(amount_of_items_input.get())))
    scan_top_ugc_of_workshop_month_button.pack()
def set_up_settings_page():
    # Create the settings frame
    settings_frame = ctk.CTkFrame(main_frame)
    settings_frame.pack(expand=True, fill="both")
    # Create the settings canvas
    settings_canvas = ctk.CTkCanvas(settings_frame)
    settings_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(settings_canvas, text="Settings", text_color='black', font=("Arial", 24))
    title_label.pack()
    # Create the back button
    back_button = ctk.CTkButton(settings_canvas, text="Back", command=lambda: load_page("Home"))
    back_button.pack()
    # Create the toggle button for "Display browser"
    display_browser_var = tk.IntVar()
    display_browser_var.set(data_functions.get_setting_value("display_browser"))
    display_browser_checkbox = tk.Checkbutton(settings_canvas, text="Display browser", variable=display_browser_var)
    display_browser_checkbox.pack()
    # Create the warning label
    warning_label = ctk.CTkLabel(settings_canvas, text="Please restart the tool to apply this setting.", text_color='red')
    warning_label.pack()
    # Create the toggle button for "Scan for comments
    scan_for_comments_var = tk.IntVar()
    scan_for_comments_var.set(data_functions.get_setting_value("comments"))
    scan_for_comments_checkbox = tk.Checkbutton(settings_canvas, text="Scan for comments", variable=scan_for_comments_var)
    scan_for_comments_checkbox.pack()
    # Create warning label
    warning_label = ctk.CTkLabel(settings_canvas, text="Warning: As the python steam api does not track comment counts, this is done via the browser, which will increase scanning time significantly.", text_color='red')
    warning_label.pack()
    # Create the toggle button for "Scan for ratings"
    scan_for_ratings_var = tk.IntVar()
    scan_for_ratings_var.set(data_functions.get_setting_value("ratings"))
    scan_for_ratings_checkbox = tk.Checkbutton(settings_canvas, text="Scan for ratings", variable=scan_for_ratings_var)
    scan_for_ratings_checkbox.pack()
    # Create warning label
    warning_label = ctk.CTkLabel(settings_canvas, text="Warning: Ratings are also tracked via the browser, increasing scanning time. They also require a valid log in.", text_color='red')
    warning_label.pack()
    # Create the apply all settings button
    def apply_all_settings():
        data_functions.apply_setting_value("display_browser", display_browser_var.get())
        data_functions.apply_setting_value("ratings", scan_for_ratings_var.get())
        data_functions.apply_setting_value("comments", scan_for_comments_var.get())
    apply_all_settings_button = ctk.CTkButton(settings_canvas, text="Apply All Settings", command=lambda: apply_all_settings())
    apply_all_settings_button.pack()
def set_up_creator_page():
    # Create the creator frame
    creator_frame = ctk.CTkFrame(main_frame)
    creator_frame.pack(expand=True, fill="both")
    # Create the creator canvas
    creator_canvas = ctk.CTkCanvas(creator_frame)
    creator_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(creator_canvas, text="Creator", text_color='black', font=("Arial", 24))
    title_label.pack()
    # Read the crator_status txt file
    creator_status_file = open("CreatorStatus.txt", "r")
    creator_status_lines = creator_status_file.readlines()
    creator_status_file.close()
    # Create the creator status listbox
    creator_status_listbox = ctk.CTkListbox(creator_canvas)
    creator_status_listbox.pack()
    for line in creator_status_lines:
        creator_status_listbox.insert("end", line)
    
    # Create the back button
    back_button = ctk.CTkButton(creator_canvas, text="Back", command=lambda: load_page("Home"))
    back_button.pack()
def set_up_steam_login_page():
    # Create the steam login frame
    steam_login_frame = ctk.CTkFrame(main_frame)
    steam_login_frame.pack(expand=True, fill="both")
    # Create the steam login canvas
    steam_login_canvas = ctk.CTkCanvas(steam_login_frame)
    steam_login_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(steam_login_canvas, text="Steam Login", text_color='black', font=("Arial", 24))
    title_label.pack()
    # Create the back button
    back_button = ctk.CTkButton(steam_login_canvas, text="Back", command=lambda: load_page("Home"))
    back_button.pack()
    # Create the username input
    username_label = ctk.CTkLabel(steam_login_canvas, text="Username", text_color='black')
    username_label.pack()
    username_input = ctk.CTkEntry(steam_login_canvas, textvariable=username_input_var, text_color='black')
    username_input.pack()
    # Create the password input
    password_label = ctk.CTkLabel(steam_login_canvas, text="Password", text_color='black')
    password_label.pack()
    password_input = ctk.CTkEntry(steam_login_canvas, show="*", textvariable=password_input_var, text_color='black')
    password_input.pack()
    # Create the login button
    login_button = ctk.CTkButton(steam_login_canvas, text="Login", command=lambda: data_functions.log_in_steam_user(username_input.get(), password_input.get(), driver))
    login_button.pack()
    # Create the verify code input
    verify_code_label = ctk.CTkLabel(steam_login_canvas, text="Verify Code", text_color='black')
    verify_code_label.pack()
    verify_code_input = ctk.CTkEntry(steam_login_canvas, textvariable=verify_code_input_var, text_color='black')
    verify_code_input.pack()
    # Create the verify code button
    verify_code_button = ctk.CTkButton(steam_login_canvas, text="Verify", command=lambda: data_functions.verify_steam_user_log_in(verify_code_input.get(), driver))
    verify_code_button.pack()

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
    elif page == "Settings":
        set_up_settings_page()
    elif page == "Creator":
        set_up_creator_page()
    elif page == "Steam Login":
        set_up_steam_login_page()
    else:
        print("Error: Page not found")
        return
    global current_page
    current_page = page  
#region input elements
date_range_start_input = tk.StringVar()
date_range_end_input = tk.StringVar()
username_input_var = tk.StringVar()
password_input_var = tk.StringVar()
verify_code_input_var = tk.StringVar()
tags_checklist_vars = {}
#endregion
#region tkinter functions
def scan_total_UGC_count_button_click():
    previous_page = current_page
    load_page("Scanning")
    app.update()
    TotalUGC.scan_for_total_UGC_count(driver)
    load_page(previous_page)
def scan_top_ugc_of_workshop_month_button_click(start_date, end_date, amount_of_items):
    previous_page = current_page
    load_page("Scanning")
    app.update()
    TopUGC.scan(driver, get_timestamp(start_date), get_timestamp(end_date), amount_of_items)
    load_page(previous_page)
def scan_total_chinese_count_button_click(start_date, end_date):
    previous_page = current_page
    load_page("Scanning")
    app.update()
    chinese_count.scan(driver, get_timestamp(start_date), get_timestamp(end_date))
    load_page(previous_page)
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

#endregion

def get_timestamp(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d")
    return int(date.timestamp())

def load_chrome_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    print(data_functions.get_setting_value("display_browser"))
    if(data_functions.get_setting_value("display_browser") == 0):
        options.add_argument("--headless")
        print("No browswer will be displayed")
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
KEY = config('STEAM_API_KEY')
steam = Steam(KEY)
url = f"https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"   
current_page = "Home"
load_page(current_page)
driver = load_chrome_driver()
wait = WebDriverWait(driver, 10)
app.mainloop()


