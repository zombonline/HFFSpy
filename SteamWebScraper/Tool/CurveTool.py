import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from steam import Steam
from datetime import datetime
from decouple import config

import TopUGC
import TotalUGC
import chinese_count
import data_functions

def set_up_header(account_name):
    for widget in header_frame.winfo_children():
        widget.destroy()
# Create the header canvas
    header_canvas = ctk.CTkCanvas(header_frame, height=50, bg='lightblue')
    header_canvas.pack(expand=False, fill="both")
# Create the header label
    if account_name:
        header_label = ctk.CTkLabel(header_canvas, text="Logged in as: " + account_name, text_color='black', font=("Arial", 24))
    else:
        header_label = ctk.CTkLabel(header_canvas, text="Not logged in", text_color='black', font=("Arial", 24))
    header_label.pack()
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
    def scan_total_UGC_count_button_click():
        previous_page = current_page
        load_page("Scanning")
        app.update()
        TotalUGC.scan_for_total_UGC_count(driver)
        load_page(previous_page)
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
    def scan_total_chinese_count_button_click(start_date, end_date):
        previous_page = current_page
        load_page("Scanning")
        app.update()
        chinese_count.scan(driver, get_timestamp(start_date), get_timestamp(end_date))
        load_page(previous_page)
    scrape_page_button = ctk.CTkButton(total_chinese_count_canvas, text="Scan", command=lambda: scan_total_chinese_count_button_click(date_range_start_input.get(), date_range_end_input.get()))
    scrape_page_button.pack()
def set_up_top_ugc_of_workshop_month_page():

    #This search may require a user to be logged in depending on settings so a check is made here.
    #If ratings are enabled and user is not logged in, the user is redirected to the steam login page.
    if data_functions.get_setting_value("ratings_levels") == 1 or data_functions.get_setting_value("ratings_models") == 1:
        if not data_functions.check_steam_user_logged_in(driver):
            load_page("Steam Login")
            return
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
    def scan_top_ugc_of_workshop_month_button_click(start_date, end_date, amount_of_items):
        previous_page = current_page
        load_page("Scanning")
        app.update()
        TopUGC.scan(driver, get_timestamp(start_date), get_timestamp(end_date), amount_of_items)
        load_page(previous_page)
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
    #Create the label "Scan for comments"
    scan_for_comments_label = ctk.CTkLabel(settings_canvas, text="Scan for comments", text_color='black')
    scan_for_comments_label.pack()
    # Create the toggle button for "Scan for comments for levels"
    scan_for_comments_levels_var = tk.IntVar()
    scan_for_comments_levels_var.set(data_functions.get_setting_value("comments_levels"))
    scan_for_comments_levels_checkbox = tk.Checkbutton(settings_canvas, text="Levels", variable=scan_for_comments_levels_var)
    scan_for_comments_levels_checkbox.pack()
    # Create the toggle button for "Scan for comments for models"
    scan_for_comments_models_var = tk.IntVar()
    scan_for_comments_models_var.set(data_functions.get_setting_value("comments_models"))
    scan_for_comments_models_checkbox = tk.Checkbutton(settings_canvas, text="Models", variable=scan_for_comments_models_var)
    scan_for_comments_models_checkbox.pack()
    # Create warning label
    warning_label = ctk.CTkLabel(settings_canvas, text="Warning: As the python steam api does not \ntrack comment counts, this is done via the browser, \nwhich will increase scanning time significantly.", text_color='red')
    warning_label.pack()
    #Create the label "Scan for ratings"
    scan_for_ratings_label = ctk.CTkLabel(settings_canvas, text="Scan for ratings", text_color='black')
    scan_for_ratings_label.pack()
    # Create the toggle button for "Scan for ratings"
    scan_for_ratings_levels_var = tk.IntVar()
    scan_for_ratings_levels_var.set(data_functions.get_setting_value("ratings_levels"))
    scan_for_ratings_levels_checkbox = tk.Checkbutton(settings_canvas, text="Levels", variable=scan_for_ratings_levels_var)
    scan_for_ratings_levels_checkbox.pack()
    # Create the toggle button for "Scan for ratings for models"
    scan_for_ratings_models_var = tk.IntVar()
    scan_for_ratings_models_var.set(data_functions.get_setting_value("ratings_models"))
    scan_for_ratings_models_checkbox = tk.Checkbutton(settings_canvas, text="Models", variable=scan_for_ratings_models_var)
    scan_for_ratings_models_checkbox.pack()
    # Create warning label
    warning_label = ctk.CTkLabel(settings_canvas, text="Warning: Ratings are also tracked via the \nbrowser, increasing scanning time. They also require \na valid log in.", text_color='red')
    warning_label.pack()
    # Create the apply all settings button
    def apply_all_settings():
        data_functions.apply_setting_value("display_browser", display_browser_var.get())
        data_functions.apply_setting_value("ratings_levels", scan_for_ratings_levels_var.get())
        data_functions.apply_setting_value("ratings_models", scan_for_ratings_models_var.get())
        data_functions.apply_setting_value("comments_levels", scan_for_comments_levels_var.get())
        data_functions.apply_setting_value("comments_models", scan_for_comments_models_var.get())

    apply_all_settings_button = ctk.CTkButton(settings_canvas, text="Apply All Settings", command=lambda: apply_all_settings())
    apply_all_settings_button.pack()
def set_up_creator_page():
    current_status = "signed"
    # Create the creator frame
    creator_frame = ctk.CTkFrame(main_frame)
    creator_frame.pack(expand=True, fill="both")
    # Create the creator canvas
    creator_canvas = ctk.CTkCanvas(creator_frame)
    creator_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(creator_canvas, text="Creator", text_color='black', font=("Arial", 24))
    title_label.pack()
     # Create the tab buttons frame
    tab_buttons_frame = ctk.CTkFrame(creator_canvas)
    tab_buttons_frame.pack()
    def populate_creator_status_listbox(status):
        current_status = status
        signed_button.configure(border_width=0)
        unsigned_button.configure(border_width=0)
        planning_to_contact_button.configure(border_width=0)
        if status == "signed":
            signed_button.configure(border_width=4)
        elif status == "contacted":
            unsigned_button.configure(border_width=4)
        elif status == "planned":
            planning_to_contact_button.configure(border_width=4)
        creator_status_listbox.delete(0, "end")
        with open(f"creator_status_{status}.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                creator_status_listbox.insert("end", line)
    #Create the 'Signed' Button
    signed_button = ctk.CTkButton(tab_buttons_frame, text="Signed", border_color="white", command=lambda: populate_creator_status_listbox("signed"))
    signed_button.grid(row=0, column=0, padx=10)
    #Create the 'Contacted' Button
    unsigned_button = ctk.CTkButton(tab_buttons_frame, text="Contacted", border_color="white", command=lambda: populate_creator_status_listbox("contacted"))
    unsigned_button.grid(row=0, column=1, padx=10)
    #Create the 'Planning to contact' Button
    planning_to_contact_button = ctk.CTkButton(tab_buttons_frame, text="Planning to contact", border_color="white", command=lambda: populate_creator_status_listbox("planned"))
    planning_to_contact_button.grid(row=0, column=2, padx=10)
    # Create the creator status listbox
    creator_status_listbox = tk.Listbox(creator_canvas)
    creator_status_listbox.pack()
    # Populate the listbox with the 'signed' creators
    populate_creator_status_listbox("signed")
    # Create the 'Add creator' input
    creator_input = ctk.CTkEntry(creator_canvas, text_color='black')
    creator_input.pack()
    # Create the 'Add creator' button
    def add_creator_button_click():
        creator_status_listbox.insert("end", creator_input.get())
        with open(f"creator_status_{current_status}.txt", "a") as file:
            file.write("\n" + creator_input.get())
        populate_creator_status_listbox(current_status)
    add_creator_button = ctk.CTkButton(creator_canvas, text="Add Creator", command=lambda: add_creator_button_click())
    add_creator_button.pack()
    # Create the 'Remove creator' button
    def remove_creator_button_click():
        creator_status_listbox.delete(creator_status_listbox.curselection())
        with open(f"creator_status_{current_status}.txt", "w") as file:
            for i in range(creator_status_listbox.size()):
                file.write(creator_status_listbox.get(i))
        populate_creator_status_listbox(current_status)
    remove_creator_button = ctk.CTkButton(creator_canvas, text="Remove Creator", command=lambda: remove_creator_button_click())
    remove_creator_button.pack()

    
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
    login_button = ctk.CTkButton(steam_login_canvas, text="Login", command=lambda: login_button_click())
    login_button.pack()
    def login_button_click():
        state = data_functions.log_in_steam_user(username_input_var.get(), password_input_var.get(), driver)
        if state == 0:
            set_up_header(username_input_var.get())
            load_page("Home")
        elif state == 1:
            # Create the verify code input
            verify_code_label = ctk.CTkLabel(steam_login_canvas, text="Verify Code", text_color='black')
            verify_code_label.pack()
            verify_code_input = ctk.CTkEntry(steam_login_canvas, textvariable=verify_code_input_var, text_color='black')
            verify_code_input.pack()
            # Create the verify code button
            def verify_code_button_click():
                data_functions.verify_steam_user_log_in(verify_code_input.get(), driver)
                set_up_header(data_functions.check_steam_user_logged_in(driver))
            verify_code_button = ctk.CTkButton(steam_login_canvas, text="Verify", command=lambda: verify_code_button_click())
            verify_code_button.pack()
        elif state == 2:
            #Create the please check steam app label
            please_check_steam_app_label = ctk.CTkLabel(steam_login_canvas, text="Please confirm log in on the Steam app", text_color='black')
            please_check_steam_app_label.pack()
            #Create the "I'm done" button
            def im_done_button_click():
                set_up_header(data_functions.check_steam_user_logged_in(driver))
                load_page("Home")
            im_done_button = ctk.CTkButton(steam_login_canvas, text="I'm done", command=lambda: im_done_button_click())
            im_done_button.pack()
        else:
            print("Error: Unknown state")   
            
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
        return None
    webdriver_service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=webdriver_service, options=options)
    return driver

app = tk.Tk()
app.title("Curve Tool")
app.geometry("400x400")

# Create the header frame
header_frame = ctk.CTkFrame(app, height=50)
header_frame.pack(expand=False, fill="both")
# Create the main frame
main_frame = ctk.CTkFrame(app)
main_frame.pack(expand=True, fill="both")

#region input elements
date_range_start_input = tk.StringVar()
date_range_end_input = tk.StringVar()
username_input_var = tk.StringVar()
password_input_var = tk.StringVar()
verify_code_input_var = tk.StringVar()
tags_checklist_vars = {}
#endregion

KEY = config('STEAM_API_KEY')
steam = Steam(KEY)
url = f"https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"   
current_page = "Home"
load_page(current_page)
set_up_header(False)
driver = load_chrome_driver()
wait = WebDriverWait(driver, 10)
app.mainloop()


