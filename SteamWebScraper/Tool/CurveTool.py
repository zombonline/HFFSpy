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
    title_label = ctk.CTkLabel(home_canvas, text="Home", font=("Arial", 24))
    title_label.pack()
    #Navigation Buttons
    total_UGC_count_button = ctk.CTkButton(home_canvas, text="Total UGC Count", command=lambda: load_page("Total UGC Count"))   
    total_UGC_count_button.pack()
    total_chinese_count_button = ctk.CTkButton(home_canvas, text="Total Chinese Count", command=lambda: load_page("Total Chinese Count"))
    total_chinese_count_button.pack()
def set_up_total_UGC_count_page():
    # Create the total UGC count frame
    total_UGC_count_frame = ctk.CTkFrame(main_frame)
    total_UGC_count_frame.pack(expand=True, fill="both")
    # Create the total UGC count canvas
    total_UGC_count_canvas = ctk.CTkCanvas(total_UGC_count_frame)
    total_UGC_count_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(total_UGC_count_canvas, text="Total UGC Count", font=("Arial", 24))
    title_label.pack()
    # Create the back button
    back_button = ctk.CTkButton(total_UGC_count_canvas, text="Back", command=lambda: load_page("Home"))
    back_button.pack()
    # Create the 'add appID' input box
    appID_input = ctk.CTkEntry(total_UGC_count_canvas,textvariable=add_appID_input)
    appID_input.pack()
    # Create the 'add appID' button
    add_appID_button = ctk.CTkButton(total_UGC_count_canvas, text="Add AppID", command=lambda: add_appID(appID_list))
    add_appID_button.pack()
    # Create the 'remove appID' button
    remove_appID_button = ctk.CTkButton(total_UGC_count_canvas, text="Remove AppID", command=lambda: remove_appID(appID_list))
    remove_appID_button.pack()
    #Create the list of appIDs
    appID_list = tk.Listbox(total_UGC_count_canvas)
    appID_list.pack()
    # Load the appIDs from the file
    populate_list_with_appIDs(appID_list)
def set_up_total_chinese_count_page():
    # Create the total Chinese count frame
    total_chinese_count_frame = ctk.CTkFrame(main_frame)
    total_chinese_count_frame.pack(expand=True, fill="both")
    # Create the total Chinese count canvas
    total_chinese_count_canvas = ctk.CTkCanvas(total_chinese_count_frame)
    total_chinese_count_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(total_chinese_count_canvas, text="Total Chinese Count", font=("Arial", 24))
    title_label.pack()
    # Create the back button
    back_button = ctk.CTkButton(total_chinese_count_canvas, text="Back", command=lambda: load_page("Home"))
    back_button.pack()    
    # Create the date range start input
    date_range_start_label = ctk.CTkLabel(total_chinese_count_canvas, text="Date Range Start")
    date_range_start_label.pack()
    date_range_start = DateEntry(total_chinese_count_canvas, textvariable=date_range_start_input, date_pattern="yyyy-mm-dd")
    date_range_start.pack()
    # Create the date range end input
    date_range_end_label = ctk.CTkLabel(total_chinese_count_canvas, text="Date Range End")
    date_range_end_label.pack()
    date_range_end = DateEntry(total_chinese_count_canvas, textvariable=date_range_end_input, date_pattern="yyyy-mm-dd")
    date_range_end.pack()
    # Create the 'submit date range' button
    submit_date_range_button = ctk.CTkButton(total_chinese_count_canvas, text="Submit Date Range", command=lambda: chinese_count_date_button_click(checkbox_frame))
    submit_date_range_button.pack()
    # Create the list of tags
    checkbox_frame = ctk.CTkFrame(total_chinese_count_canvas)
    checkbox_frame.pack()
    #Create the 'submit tags' button
    submit_tags_button = ctk.CTkButton(total_chinese_count_canvas, text="Submit Tags", command=lambda: chinese_count_submit_tags_button_click(checkbox_frame))
    submit_tags_button.pack()

   

def load_page(page):
    for widget in main_frame.winfo_children():
        widget.destroy()
    if page == "Home":
        set_up_home_page()
    elif page == "Total UGC Count":
        set_up_total_UGC_count_page()
    elif page == "Total Chinese Count":
        set_up_total_chinese_count_page()
    else:
        print("Error: Page not found")

#region input elements
add_appID_input = tk.StringVar()
date_range_start_input = tk.StringVar()
date_range_end_input = tk.StringVar()
tags_checklist_vars = []
#endregion
#region tkinter functions
def populate_list_with_appIDs(list):
    list.delete(0, tk.END)  
    this_dir = os.path.dirname(os.path.abspath(__file__))
    file = open(f"{this_dir}/UGCTotalAppIDs.txt", "r")
    for line in file:
        list.insert(tk.END, line)
    file.close()
def add_appID(list):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    file = open(f"{this_dir}/UGCTotalAppIDs.txt", "a")
    print(add_appID_input.get())
    if add_appID_input.get() != "":
        print("Wrote to file")
        file.write(add_appID_input.get() + "\n")
    file.close()
    populate_list_with_appIDs(list)
def remove_appID(list):
    selected_index = get_selected_list_element_index(list)
    if selected_index != None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        file = open(f"{this_dir}/UGCTotalAppIDs.txt", "r")
        lines = file.readlines()
        file.close()
        file = open(f"{this_dir}/UGCTotalAppIDs.txt", "w")
        for i in range(len(lines)):
            if i != selected_index:
                file.write(lines[i]) 
        file.close()   
        populate_list_with_appIDs(list)
def get_selected_list_element_index(list):
    selected_indices = list.curselection()
    if selected_indices:  # if there is a selection
        first_selected_index = selected_indices[0]
        print(first_selected_index)
        return first_selected_index
    else:
        return None
def create_checklist(options, canvas):
    vars = []
    for i in range(len(options)):
        var = tk.IntVar()
        vars.append(var)
        options[i] = tk.Checkbutton(canvas, text=options[i], variable=var, onvalue=1, offvalue=0)
        options[i].grid(column=i//7, row=i%7)
    return vars
def chinese_count_date_button_click(canvas):
    submit_date_range_to_url(date_range_start_input.get(), date_range_end_input.get())
    tags_checklist_vars = create_checklist(load_tags_from_webpage(), canvas)
def chinese_count_submit_tags_button_click(canvas):
    tags = []
    for i in range(len(tags_checklist_vars)):
        if tags_checklist_vars[i].get() == 1:
            tags.append(tags_checklist_vars[i].cget("text"))
    print(tags)
    print("done")
    #endregion
    #region selenium functions
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


load_page("Home")
driver = load_chrome_driver()
wait = WebDriverWait(driver, 10)
app.mainloop()


