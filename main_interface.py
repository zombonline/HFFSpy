import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry
import os
from datetime import datetime, timedelta
import gen_top_item_in_date_range
import gen_most_played_workshop_games
import gen_total_items_in_date_range
import main_functions
import threading
import queue
import sys
import time

def set_up_header(account_name):
    for widget in header_frame.winfo_children():
        widget.destroy()
# Create the header canvas
    header_canvas = ctk.CTkCanvas(header_frame, height=65, bg='orange')
    header_canvas.pack(expand=False, fill="both")
# Create the header label
    if account_name:
        header_label = ctk.CTkLabel(header_canvas, text="Logged in as: " + account_name, text_color='black', font=("Arial", 18))
    else:
        header_label = ctk.CTkLabel(header_canvas, text="Not logged in", text_color='black', font=("Arial", 18))
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
    # Create the "Scans" label
    scans_label = ctk.CTkLabel(home_canvas, text="Scans", text_color='black', font=("Arial", 18))
    scans_label.pack(pady=10)
    #Navigation Buttons
    total_UGC_count_button = ctk.CTkButton(home_canvas, text="Top 100 Games (UGC Count)", command=lambda: load_page("Total UGC Count"))   
    total_UGC_count_button.pack(pady=5)
    top_ugc_of_workshop_month_button = ctk.CTkButton(home_canvas, text="Top Rated HFF Workshop items", command=lambda: load_page("Top Monthly Workshop Items"))
    top_ugc_of_workshop_month_button.pack(pady=5)
    # Create the "Other" label
    other_label = ctk.CTkLabel(home_canvas, text="Other", text_color='black', font=("Arial", 18))
    other_label.pack(pady=10)
    #Create the 'Download Chromdriver here' button
    download_chromedriver_button = ctk.CTkButton(home_canvas, text="Download Chromedriver here", command=lambda: os.system("start https://googlechromelabs.github.io/chrome-for-testing/"))
    download_chromedriver_button.pack(pady=5)
    settings_button = ctk.CTkButton(home_canvas, text="Settings", command=lambda: load_page("Settings"))
    settings_button.pack(pady=5)
    creator_button = ctk.CTkButton(home_canvas, text="Creator", command=lambda: load_page("Creator"))
    creator_button.pack(pady=5)
    steam_login_button = ctk.CTkButton(home_canvas, text="Steam Login", command=lambda: load_page("Steam Login"))
    steam_login_button.pack(pady=5)
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
    # Create the progress message label
    progress_message_label = ctk.CTkLabel(loading_canvas, text="This may take a while", text_color='black')
    progress_message_label.pack()
    def update_progress():
        try:
            while True:
                msg = progress_queue.get_nowait()
                progress_message_label.configure(text=msg)
        except queue.Empty:
            pass
        if active_thread.is_alive():
            app.after(100, update_progress)
        else:
            loading_label.configure(text="Scanning complete")
            # Create the back button
            back_button = ctk.CTkButton(loading_canvas, text="Back", command=lambda: load_page("Home"))
            back_button.pack()
    app.after(100, update_progress)
def set_up_most_played_workshop_games_page():
    # Create the total UGC count frame
    total_UGC_count_frame = ctk.CTkFrame(main_frame)
    total_UGC_count_frame.pack(expand=True, fill="both")
    # Create the total UGC count canvas
    total_UGC_count_canvas = ctk.CTkCanvas(total_UGC_count_frame)
    total_UGC_count_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(total_UGC_count_canvas, text="Top 100 Games (UGC Count)", text_color='black', font=("Arial", 24))
    title_label.pack()
    # Create the info label
    info_label = ctk.CTkLabel(total_UGC_count_canvas, text="This will scan the current top 100 most played workshop games and display the total UGC count.", wraplength = 200, text_color='black')
    info_label.pack()
    # Create the back button
    back_button = ctk.CTkButton(total_UGC_count_canvas, text="Back", command=lambda: load_page("Home"))
    back_button.pack(pady=10)
    # Create the scan total UGC count button

def set_up_top_items_in_date_range_page():
    # Create the top monthly workshop items frame
    top_monthly_workshop_items_frame = ctk.CTkCanvas(main_frame, bg='grey')
    top_monthly_workshop_items_frame.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(top_monthly_workshop_items_frame, text="Top Rated HFF Workshop items", text_color='black', font=("Arial", 24))
    title_label.pack(pady=10)
    # Create the info label
    info_label = ctk.CTkLabel(top_monthly_workshop_items_frame, text="This will scan the specified amount of items on the workshop within the provided date range. They will be listed by 'Most Popular' on steam.", wraplength = 200, text_color='black')
    info_label.pack()
    # Create the back button
    back_button = ctk.CTkButton(top_monthly_workshop_items_frame, text="Back", command=lambda: load_page("Home"))
    back_button.pack(pady=10)
    # Create the weekly scan button
    def weekly_settings():
        #Get the last full week
        start = datetime.now() - timedelta(days=datetime.now().weekday() + 7)
        end = datetime.now() - timedelta(days=datetime.now().weekday() + 1)
        date_range_start_var.set(start.date())
        date_range_end_var.set(end.date())
        amount_of_items_input.delete(0, "end")
        sort_by_dropdown.set("Most Recent")
        seperate_levels_and_models_var.set(False)
        outputs = ['Item Name', 'Creator Name', 'Item Type','Country', 'Language', 'Date Posted']
        for item in excel_outputs:
            if item in outputs:
                excel_outputs[item][1].set(True)
            else:
                excel_outputs[item][1].set(False)
    weekly_settings_button = ctk.CTkButton(top_monthly_workshop_items_frame, text="Weekly Scan", command=lambda: weekly_settings())
    weekly_settings_button.pack(pady=10)
    # Create the monthly scan button
    def monthly_settings():
        # Get the last full month
        start = (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1)
        end = datetime.now().replace(day=1) - timedelta(days=1)
        date_range_start_var.set(start.date())
        date_range_end_var.set(end.date())
        amount_of_items_input.delete(0, "end")
        amount_of_items_input.insert(0, "20")
        sort_by_dropdown.set("Most Popular")
        seperate_levels_and_models_var.set(True)
        outputs = ['Item Name', 'Creator Name', 'Item Type','Country', 'Language', 'Date Posted', 'TUS', 'Rating', 'Comment Count', 'Visitors']
        for item in excel_outputs:
            if item in outputs:
                excel_outputs[item][1].set(True)
            else:
                excel_outputs[item][1].set(False)
    monthly_settings_button = ctk.CTkButton(top_monthly_workshop_items_frame, text="Monthly Scan", command=lambda: monthly_settings())
    monthly_settings_button.pack(pady=10)

    # Create the options frame
    options_frame = ctk.CTkFrame(top_monthly_workshop_items_frame,fg_color='transparent')
    options_frame.pack(pady=10)
    # Create the general options frame
    general_options_frame = ctk.CTkFrame(options_frame,fg_color='transparent')
    general_options_frame.grid(row=0, column=0)
    # Create the include in excel frame
    include_in_excel_frame = ctk.CTkFrame(options_frame, fg_color='transparent')
    include_in_excel_frame.grid(row=0, column=1, padx=10)


    # Create the date range start input
    date_range_start_label = ctk.CTkLabel(general_options_frame, text="From:", text_color='white')
    date_range_start_label.pack()
    # Create the date range start variable
    date_range_start_var = tk.StringVar()
    # Create the date range start input
    date_range_start_input = DateEntry(general_options_frame, textvariable=date_range_start_var, date_pattern="yyyy-mm-dd")
    date_range_start_input.pack()
    # Create the date range end input
    date_range_end_label = ctk.CTkLabel(general_options_frame, text="Until:", text_color='white')
    date_range_end_label.pack()
    # Create the date range end variable
    date_range_end_var = tk.StringVar()
    # Create the date range end input
    date_range_end_input = DateEntry(general_options_frame, textvariable=date_range_end_var, date_pattern="yyyy-mm-dd")
    date_range_end_input.pack()
    # Create the amount of items to grab input
    amount_of_items_label = ctk.CTkLabel(general_options_frame, text="Amount of Items to Grab", text_color='white')
    amount_of_items_label.pack()
    # Create the amount of items input
    amount_of_items_input = ctk.CTkEntry(general_options_frame)
    amount_of_items_input.insert(0, "20")
    amount_of_items_input.pack()
    # Create the sort by label
    sort_by_label = ctk.CTkLabel(general_options_frame, text="Sort by", text_color='white')
    sort_by_label.pack()
    # Initialize the variable to hold the selected option
    sort_by_var = tk.StringVar()
    # Create the sort by dropdown
    sort_by_dropdown = ctk.CTkOptionMenu(general_options_frame, variable=sort_by_var, values=["Most Popular", "Most Recent"])
    sort_by_dropdown.pack()
    # Set the default value
    sort_by_var.set("Most Popular")
    # Create the seperate levels and models checkbox
    seperate_levels_and_models_var = tk.BooleanVar()
    seperate_levels_and_models_var.set(True)
    seperate_levels_and_models_checkbox = ctk.CTkCheckBox(general_options_frame, text="Seperate levels and models", variable=seperate_levels_and_models_var)
    seperate_levels_and_models_checkbox.pack(pady=10)

    # Create the include in excel label
    include_in_excel_label = ctk.CTkLabel(include_in_excel_frame, text="Inlcude in Excel", text_color='white')
    include_in_excel_label.pack()
    # Create the excel format checkboxes
    excel_outputs = {
        'Item Name': ['title', tk.BooleanVar()],
        'Creator ID': ['creator_id', tk.BooleanVar()],
        'Creator Name': ['creator_name', tk.BooleanVar()],
        'Date Posted': ['date_posted', tk.BooleanVar()],
        'Country': ['country', tk.BooleanVar()],
        'Language': ['language', tk.BooleanVar()],
        'TUS': ['tus', tk.BooleanVar()],
        'Rating': ['rating', tk.BooleanVar()],
        'Comment Count': ['comment_count', tk.BooleanVar()],
        'Tags': ['tags', tk.BooleanVar()],
        'Item Type': ['item_type', tk.BooleanVar()],
        'Contribution Count': ['contribution_count', tk.BooleanVar()],
        'Followers': ['followers', tk.BooleanVar()],
        'Visitors': ['visitors', tk.BooleanVar()]
    }
    intensive_outputs = ['Rating', 'Comment Count', 'Contribution Count', 'Followers', 'Visitors']
    for item in excel_outputs:
        excel_outputs[item][1].set(True)
        output_color = 'white'
        if item in intensive_outputs:
            excel_outputs[item][1].set(False)
            output_color = 'orange'
        checkbox = ctk.CTkCheckBox(include_in_excel_frame, text=item, variable=excel_outputs[item][1], text_color=output_color)
        checkbox.pack(anchor="w", pady=2)

    def scan_top_ugc_of_workshop_month_button_click():
        global active_thread
        start_date = get_timestamp(date_range_start_var.get())
        end_date = get_timestamp(date_range_end_var.get(), True)
        amount_of_items = None
        if amount_of_items_input.get() != "":
            amount_of_items = int(amount_of_items_input.get())
        sort_by = sort_by_var.get()
        seperate_levels_and_models = seperate_levels_and_models_var.get()
        for item in excel_outputs:
            excel_outputs[item][1] = excel_outputs[item][1].get()
        
        active_thread = threading.Thread(target=gen_top_item_in_date_range.scan, args=(start_date, end_date, amount_of_items, sort_by, seperate_levels_and_models, excel_outputs, progress_queue))
        active_thread.start()
        load_page("Scanning")
        app.update()
    
    scan_top_ugc_of_workshop_month_button = ctk.CTkButton(top_monthly_workshop_items_frame, text="Scan", command=lambda: scan_top_ugc_of_workshop_month_button_click())
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
    display_browser_var.set(main_functions.get_setting_value("display_browser"))
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
    scan_for_comments_levels_var.set(main_functions.get_setting_value("comments_levels"))
    scan_for_comments_levels_checkbox = tk.Checkbutton(settings_canvas, text="Levels", variable=scan_for_comments_levels_var)
    scan_for_comments_levels_checkbox.pack()
    # Create the toggle button for "Scan for comments for models"
    scan_for_comments_models_var = tk.IntVar()
    scan_for_comments_models_var.set(main_functions.get_setting_value("comments_models"))
    scan_for_comments_models_checkbox = tk.Checkbutton(settings_canvas, text="Models", variable=scan_for_comments_models_var)
    scan_for_comments_models_checkbox.pack()
    # Create warning label
    warning_label = ctk.CTkLabel(settings_canvas, text="Warning: As the python steam api does not track comment counts, this is done via the browser, which will increase scanning time significantly.", wraplength=200, text_color='red')
    warning_label.pack()
    #Create the label "Scan for ratings"
    scan_for_ratings_label = ctk.CTkLabel(settings_canvas, text="Scan for ratings", text_color='black')
    scan_for_ratings_label.pack()
    # Create the toggle button for "Scan for ratings"
    scan_for_ratings_levels_var = tk.IntVar()
    scan_for_ratings_levels_var.set(main_functions.get_setting_value("ratings_levels"))
    scan_for_ratings_levels_checkbox = tk.Checkbutton(settings_canvas, text="Levels", variable=scan_for_ratings_levels_var)
    scan_for_ratings_levels_checkbox.pack()
    # Create the toggle button for "Scan for ratings for models"
    scan_for_ratings_models_var = tk.IntVar()
    scan_for_ratings_models_var.set(main_functions.get_setting_value("ratings_models"))
    scan_for_ratings_models_checkbox = tk.Checkbutton(settings_canvas, text="Models", variable=scan_for_ratings_models_var)
    scan_for_ratings_models_checkbox.pack()
    # Create warning label
    warning_label = ctk.CTkLabel(settings_canvas, text="Warning: Ratings are also tracked via the browser, increasing scanning time. They also require a valid log in.", wraplength=200, text_color='red')
    warning_label.pack()
    # Create the apply all settings button
    def apply_all_settings():
        main_functions.apply_setting_value("display_browser", display_browser_var.get())
        main_functions.apply_setting_value("ratings_levels", scan_for_ratings_levels_var.get())
        main_functions.apply_setting_value("ratings_models", scan_for_ratings_models_var.get())
        main_functions.apply_setting_value("comments_levels", scan_for_comments_levels_var.get())
        main_functions.apply_setting_value("comments_models", scan_for_comments_models_var.get())
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
        global current_status 
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
                if line == "\n":
                    continue
                user_details = main_functions.get_user_details(line)
                if user_details == None:
                    continue
                creator_status_listbox.insert("end", main_functions.get_item_creator_name(user_details)  + " (" + line + ")")
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
    creator_status_listbox = tk.Listbox(creator_canvas, width=50)
    creator_status_listbox.pack()
    # Populate the listbox with the 'signed' creators
    populate_creator_status_listbox("signed")
    # Create the message label
    message_label = ctk.CTkLabel(creator_canvas, text="", text_color='black', font=("Arial", 24))
    message_label.pack()
    # Create the 'Add creator' input
    creator_input = ctk.CTkEntry(creator_canvas, text_color='white')
    creator_input.pack()
    # Create the 'Add creator' button
    def add_creator_button_click():
        global current_status
        creator_id = creator_input.get()
        if main_functions.get_user_details(creator_id) == None:
            message_label.configure(text="Error: User not found", text_color='red')
            print("Error: User not found")
        else:
            message_label.configure(text="User succesfully added to " + current_status + " list", text_color='green')
            with open(f"creator_status_{current_status}.txt", "r") as oldfile, open(f"creator_status_{current_status}_temp.txt", "w") as newfile:
                for line in oldfile:
                    newfile.write(line)
                newfile.write(creator_id + "\n")
            os.remove(f"creator_status_{current_status}.txt")
            os.rename(f"creator_status_{current_status}_temp.txt", f"creator_status_{current_status}.txt")
            populate_creator_status_listbox(current_status)
            creator_input.delete(0, "end")
    add_creator_button = ctk.CTkButton(creator_canvas, text="Add Creator", command=lambda: add_creator_button_click())
    add_creator_button.pack()
    # Create the 'Remove creator' button
    def remove_creator_button_click():
        global current_status
        # Get position of selected item
        selected_item_index = creator_status_listbox.curselection()[0]
        message_label.configure(text="User succesfully removed from " + current_status + " list", text_color='green')
        with open(f"creator_status_{current_status}.txt", "r") as oldfile, open(f"creator_status_{current_status}_temp.txt", "w") as newfile:
            for index, line in enumerate(oldfile):
                if index == selected_item_index or line == "\n":
                    continue
                newfile.write(line)
        os.remove(f"creator_status_{current_status}.txt")
        os.rename(f"creator_status_{current_status}_temp.txt", f"creator_status_{current_status}.txt")
            
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
    username_input = ctk.CTkEntry(steam_login_canvas, textvariable=username_input_var, text_color='white')
    username_input.pack()
    # Create the password input
    password_label = ctk.CTkLabel(steam_login_canvas, text="Password", text_color='black')
    password_label.pack()
    password_input = ctk.CTkEntry(steam_login_canvas, show="*", textvariable=password_input_var, text_color='white')
    password_input.pack()
    # Create the login button
    login_button = ctk.CTkButton(steam_login_canvas, text="Login", command=lambda: login_button_click())
    login_button.pack()
    def login_button_click():
        state = main_functions.log_in_steam_user(username_input_var.get(), password_input_var.get())
        if state == 0:
            #User already logged in
            set_up_header(main_functions.check_steam_user_logged_in())
            load_page("Home")
        elif state == 1:
            set_up_header(username_input_var.get())
            load_page("Home")
        elif state == 2:
            # Create the verify code input
            verify_code_label = ctk.CTkLabel(steam_login_canvas, text="Verify Code", text_color='black')
            verify_code_label.pack()
            verify_code_input = ctk.CTkEntry(steam_login_canvas, textvariable=verify_code_input_var, text_color='white')
            verify_code_input.pack()
            # Create the verify code button
            def verify_code_button_click():
                main_functions.verify_steam_user_log_in(verify_code_input.get())
                set_up_header(main_functions.check_steam_user_logged_in())
            verify_code_button = ctk.CTkButton(steam_login_canvas, text="Verify", command=lambda: verify_code_button_click())
            verify_code_button.pack()
        elif state == 3:
            #Create the please check steam app label
            please_check_steam_app_label = ctk.CTkLabel(steam_login_canvas, text="Please confirm log in on the Steam app", text_color='black')
            please_check_steam_app_label.pack()
            #Create the "I'm done" button
            def im_done_button_click():
                set_up_header(main_functions.check_steam_user_logged_in())
                load_page("Home")
            im_done_button = ctk.CTkButton(steam_login_canvas, text="I'm done", command=lambda: im_done_button_click())
            im_done_button.pack()
        else:
            print("Error: Unknown state")   
def set_up_chrome_driver_page():
    # Create the chrome driver frame
    chrome_driver_frame = ctk.CTkFrame(main_frame)
    chrome_driver_frame.pack(expand=True, fill="both")
    # Create the chrome driver canvas
    chrome_driver_canvas = ctk.CTkCanvas(chrome_driver_frame)
    chrome_driver_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(chrome_driver_canvas, text="Chrome Driver", text_color='black', font=("Arial", 24))
    title_label.pack()
    # Create the info label
    info_label = ctk.CTkLabel(chrome_driver_canvas, text="There may have been an error with your Chrome Driver. Please ensure you have a chrome driver installed in the program folder and the version matches your current installation of Google Chrome. Once done, please restart the program.", wraplength = 200, text_color='black')
    info_label.pack()
    # Create the download button
    download_button = ctk.CTkButton(chrome_driver_canvas, text="Download", command=lambda: os.system("start https://googlechromelabs.github.io/chrome-for-testing/"))
    download_button.pack()
def set_up_add_api_key_page():
    # Create the add api key frame
    add_api_key_frame = ctk.CTkFrame(main_frame)
    add_api_key_frame.pack(expand=True, fill="both")
    # Create the add api key canvas
    add_api_key_canvas = ctk.CTkCanvas(add_api_key_frame)
    add_api_key_canvas.pack(expand=True, fill="both")
    # Create the title
    title_label = ctk.CTkLabel(add_api_key_canvas, text="INVALID API KEY", text_color='black', font=("Arial", 24))
    title_label.pack()
    # Create the info label
    info_label = ctk.CTkLabel(add_api_key_canvas, text="Please enter a valid steam API key", wraplength = 200, text_color='black')
    info_label.pack()
    # Create the api key input
    api_key_input = ctk.CTkEntry(add_api_key_canvas, text_color='white')
    api_key_input.pack()
    # Create the submit button
    def submit_button_click():
        main_functions.apply_setting_value("steam_api_key", api_key_input.get())
        if(main_functions.set_steam_api_key() == True):
            load_page("Home")
        else:
            api_key_input.delete(0, "end")
    submit_button = ctk.CTkButton(add_api_key_canvas, text="Submit", command=lambda: submit_button_click())
    submit_button.pack()

def load_page(page):
    for widget in main_frame.winfo_children():
        widget.destroy()
    if page == "Home":
        set_up_home_page()
    elif page == "Total UGC Count":
        set_up_most_played_workshop_games_page()
    elif page == "Top Monthly Workshop Items":
        set_up_top_items_in_date_range_page()
    elif page == "Scanning":
        set_up_scanning_page()
    elif page == "Settings":
        set_up_settings_page()
    elif page == "Creator":
        set_up_creator_page()
    elif page == "Steam Login":
        set_up_steam_login_page()
    elif page == "Chrome Driver":
        set_up_chrome_driver_page()
    elif page == "Add API Key":
        set_up_add_api_key_page()
    else:
        print("Error: Page not found")
        return
    global current_page
    current_page = page  

def get_timestamp(date_string, end_of_day=False):
    date = datetime.strptime(date_string, "%Y-%m-%d")
    if end_of_day:
        return int(date.replace(hour=23, minute=59, second=59).timestamp())
    return int(date.timestamp())

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

app = tk.Tk()
app.title("HFFSpy")
icon_path = get_resource_path("icon.ico")
app.iconbitmap(icon_path)
app.geometry("600x750")
app.minsize(600, 500)

# Create the header frame
header_frame = ctk.CTkFrame(app, height=65)
header_frame.pack(expand=False, fill="both")
# Create the main frame
main_frame = ctk.CTkFrame(app)
main_frame.pack(expand=True, fill="both")

progress_queue = queue.Queue()


username_input_var = tk.StringVar()
password_input_var = tk.StringVar()
verify_code_input_var = tk.StringVar()
tags_checklist_vars = {}

active_thread = None
#endregion
 
current_page = "Home"
load_page(current_page)
set_up_header(False)
main_functions.check_for_creator_status_file()
main_functions.check_for_settings_file()
main_functions.populate_user_lists()

if(main_functions.start_driver() == False):
    load_page("Chrome Driver")
elif(main_functions.set_steam_api_key() == False):
    load_page("Add API Key")

app.mainloop()