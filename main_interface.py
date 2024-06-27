import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry
import os
from datetime import datetime, timedelta
import gen_top_item_in_date_range
import gen_most_played_workshop_games
import main_functions
import threading
import queue
import sys

def set_up_header(account_name):
    for widget in header_canvas.winfo_children():
        widget.destroy()
    # Create the header label
    if account_name:
        header_label = ctk.CTkLabel(header_canvas, text="Logged in as: " + account_name, text_color='black', font=("Arial", 18))
    else:
        header_label = ctk.CTkLabel(header_canvas, text="Not logged in", text_color='black', font=("Arial", 18))
    header_label.pack(pady=5)

def set_up_page_canvas(page_name, page_info, include_home_button):
    new_canvas = ctk.CTkCanvas(main_canvas, bg='grey')
    new_canvas.pack(expand=True, fill="both")
    new_title = ctk.CTkLabel(new_canvas, text=page_name, text_color='black', font=("Arial", 24))
    new_title.pack(pady=5)
    if page_info != None:
        new_info = ctk.CTkLabel(new_canvas, text=page_info, wraplength = app.winfo_width()-10, text_color='black')
        new_info.pack(pady=5)
    if include_home_button:
        # Create the back button
        home_button = ctk.CTkButton(new_canvas, text="Back", command=lambda: load_page("Home"))
        home_button.pack(pady=5)
    return new_canvas

def set_up_home_page():
    home_canvas = set_up_page_canvas("Home", None, False)
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
    creator_button = ctk.CTkButton(home_canvas, text="Creator", command=lambda: load_page("Creator"))
    creator_button.pack(pady=5)
    steam_login_button = ctk.CTkButton(home_canvas, text="Steam Login", command=lambda: load_page("Steam Login"))
    steam_login_button.pack(pady=5)
    
    # Create the toggle button for "Display browser"
    def enable_display_browser():
        main_functions.apply_setting_value("display_browser", display_browser_var.get())
        warning_label.configure(text="Please restart the program for changes to take effect")
    display_browser_var = tk.IntVar()
    display_browser_var.set(main_functions.get_setting_value("display_browser"))
    display_browser_checkbox = ctk.CTkCheckBox(home_canvas, text="Display browser", variable=display_browser_var, command=lambda: enable_display_browser())
    display_browser_checkbox.pack()
    warning_label = ctk.CTkLabel(home_canvas, text="", text_color='red')
    warning_label.pack()
def set_up_scanning_page():
    loading_canvas = set_up_page_canvas("Scanning", None, False)
    progress_message_label = ctk.CTkLabel(loading_canvas, text="This may take a while", text_color='black',)
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
            progress_message_label.configure(text="Scanning complete")
            # Create the back button
            back_button = ctk.CTkButton(loading_canvas, text="Back", command=lambda: load_page("Home"))
            back_button.pack()
    app.after(100, update_progress)
def set_up_most_played_workshop_games_page():
    total_UGC_count_info = "This will scan the current top 100 most played workshop games and display the total UGC count."
    total_UGC_count_canvas = set_up_page_canvas("Total UGC Count", total_UGC_count_info, True)
    # Create the scan total UGC count button
    def scan_total_UGC_count_button_click():
        global active_thread
        active_thread = threading.Thread(target=gen_most_played_workshop_games.scan, args=(progress_queue,))
        active_thread.start()
        load_page("Scanning")
        app.update()
    scan_total_UGC_count_button = ctk.CTkButton(total_UGC_count_canvas, text="Scan Total UGC Count", command=lambda: scan_total_UGC_count_button_click())
    scan_total_UGC_count_button.pack()
def set_up_top_items_in_date_range_page():
    hff_workshop_scan_info = "You can use this page to scan the Human Fall Flat Workshop! Set a custom date range, max amount of items to return (blank will return all of them), and sort by 'Most Popular' or 'Most Recent'. You can also choose to seperate levels and models in to two different sheets. Select what information you want to include in the excel file, some may increase the time of the scan or require a logged in steam account. When the scan is complete you will be given an excel file."
    hff_scan_canvas = set_up_page_canvas("HFF Scan", hff_workshop_scan_info, True)
    # Create the scan presets frame
    scan_presets_frame = ctk.CTkFrame(hff_scan_canvas,fg_color='transparent')
    scan_presets_frame.pack(pady=10)
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
    weekly_settings_button = ctk.CTkButton(scan_presets_frame, text="Weekly Scan", command=lambda: weekly_settings())
    weekly_settings_button.grid(row=0, column=0, padx=5)
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
    monthly_settings_button = ctk.CTkButton(scan_presets_frame, text="Monthly Scan", command=lambda: monthly_settings())
    monthly_settings_button.grid(row=0, column=1, padx=5)

    # Create the options frame
    options_frame = ctk.CTkFrame(hff_scan_canvas,fg_color='transparent')
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
    login_required_outputs = ['Rating', 'Visitors']
    for item in excel_outputs:
        excel_outputs[item][1].set(True)
        checkbox_text = item
        checkbox_text_color = 'white'
        if item in intensive_outputs:
            checkbox_text += " (Intensive)"
            checkbox_text_color = 'orange'
        if item in login_required_outputs:
            checkbox_text += " (Login Required)"
            checkbox_text_color = 'orange'
        checkbox = ctk.CTkCheckBox(include_in_excel_frame, text=checkbox_text, variable=excel_outputs[item][1], text_color=checkbox_text_color)
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
            if excel_outputs[item][1] == True:
                if item in login_required_outputs and main_functions.check_steam_user_logged_in() == False:
                    print("Error: User not logged in")
                    return
        active_thread = threading.Thread(target=gen_top_item_in_date_range.scan, args=(start_date, end_date, amount_of_items, sort_by, seperate_levels_and_models, excel_outputs, progress_queue))
        active_thread.start()
        load_page("Scanning")
        app.update()
    
    scan_top_ugc_of_workshop_month_button = ctk.CTkButton(hff_scan_canvas, text="Scan", command=lambda: scan_top_ugc_of_workshop_month_button_click())
    scan_top_ugc_of_workshop_month_button.pack()
def set_up_creator_page():
    creator_info = "You can note down known creators here, any noted creators will be hilighted in the excel files generated by this tool."
    creator_canvas = set_up_page_canvas("Creator", creator_info, True)
    tab_buttons_frame = ctk.CTkFrame(creator_canvas, fg_color='transparent')
    tab_buttons_frame.pack(pady=5)
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
                creator_status_listbox.insert("end", line.strip())
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
    creator_status_listbox = tk.Listbox(creator_canvas, width=50, selectmode="single", bg='darkgray', relief="flat", justify="center",activestyle="none")
    creator_status_listbox.pack()
    # Populate the listbox with the 'signed' creators
    populate_creator_status_listbox("signed")
    # Create the message label
    message_label = ctk.CTkLabel(creator_canvas, text="", text_color='black', font=("Arial", 24))
    message_label.pack()
    # Create the 'Add creator' input
    creator_input = ctk.CTkEntry(creator_canvas, text_color='white', placeholder_text="Enter a Steam User ID")
    creator_input.pack()
    # Create the 'Add creator' button
    def add_creator_button_click():
        global current_status
        creator_id = creator_input.get()
        user = main_functions.get_user_details(creator_id)
        if user == None:
            message_label.configure(text="Error: User not found", text_color='red')
            print("Error: User not found")
        else:
            message_label.configure(text="User succesfully added to " + current_status + " list", text_color='green')
            with open(f"creator_status_{current_status}.txt", "r") as oldfile, open(f"creator_status_{current_status}_temp.txt", "w") as newfile:
                for line in oldfile:
                    newfile.write(line)
                
                newfile.write(main_functions.get_creator_name(user) + " (" + creator_id + ")\n")
            os.remove(f"creator_status_{current_status}.txt")
            os.rename(f"creator_status_{current_status}_temp.txt", f"creator_status_{current_status}.txt")
            populate_creator_status_listbox(current_status)
            creator_input.delete(0, "end")
        main_functions.populate_user_lists()

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
        main_functions.populate_user_lists()
    remove_creator_button = ctk.CTkButton(creator_canvas, text="Remove Creator", command=lambda: remove_creator_button_click())
    remove_creator_button.pack()
def set_up_steam_login_page():
    steam_login_info = "Use this page to log in to a steam account that has permission to view extra information on Human Fall Flat workshop items. This is required for a couple of bits of information such as ratings and visitor count etc.\n\n Please ensure the steam account uses English or Simplified Chinese as it's language to allow scans to function correctly."
    steam_login_canvas = set_up_page_canvas("Steam Login", steam_login_info, True)

    username_input_var = tk.StringVar()
    password_input_var = tk.StringVar()
    verify_code_input_var = tk.StringVar()

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
    login_button.pack(pady=5)
    def login_button_click():
        global active_thread
        global progress_queue
        state = main_functions.log_in_steam_user(username_input_var.get(), password_input_var.get(), progress_queue)
        if state == 0:
            #User already logged in
            set_up_header(main_functions.check_steam_user_logged_in(progress_queue))
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
                main_functions.verify_steam_user_log_in(verify_code_input.get(), progress_queue)
                set_up_header(main_functions.check_steam_user_logged_in(progress_queue))
            verify_code_button = ctk.CTkButton(steam_login_canvas, text="Verify", command=lambda: verify_code_button_click())
            verify_code_button.pack()
        elif state == 3:
            #Create the please check steam app label
            please_check_steam_app_label = ctk.CTkLabel(steam_login_canvas, text="Please confirm log in on the Steam app", text_color='black')
            please_check_steam_app_label.pack()
            #Create the "I'm done" button
            def im_done_button_click():
                set_up_header(main_functions.check_steam_user_logged_in(progress_queue))
                load_page("Home")
            im_done_button = ctk.CTkButton(steam_login_canvas, text="I'm done", command=lambda: im_done_button_click())
            im_done_button.pack()
        else:
            print("Error: Unknown state")   
    
def set_up_chrome_driver_page():
    chrome_driver_info = "There may have been an error with locating your Chrome Driver. Please ensure you have a chrome driver installed in the program folder and the version matches your current installation of Google Chrome. Once done, please restart the program."
    chrome_driver_canvas = set_up_page_canvas("Chrome Driver", chrome_driver_info, False)
    # Create the download button
    download_button = ctk.CTkButton(chrome_driver_canvas, text="Download", command=lambda: os.system("start https://googlechromelabs.github.io/chrome-for-testing/"))
    download_button.pack()
    # Create the 'open program folder' button
    open_program_folder_button = ctk.CTkButton(chrome_driver_canvas, text="Open Program Folder", command=lambda: os.system("start ."))
    open_program_folder_button.pack(pady=5)
def set_up_add_api_key_page():
    api_key_info = "Please enter a valid steam API key."
    add_api_key_canvas = set_up_page_canvas("Add API Key", api_key_info, False)
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
    for widget in main_canvas.winfo_children():
        widget.destroy()
    if page == "Home":
        set_up_home_page()
    elif page == "Total UGC Count":
        set_up_most_played_workshop_games_page()
    elif page == "Top Monthly Workshop Items":
        set_up_top_items_in_date_range_page()
    elif page == "Scanning":
        set_up_scanning_page()
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

# App Setup
app = tk.Tk()
app.title("HFFSpy")
icon_path = get_resource_path("icon.ico")
app.iconbitmap(icon_path)
app.geometry("600x750")
app.minsize(600, 750)
app.maxsize(600, 750)

# Create the header frame
header_canvas = ctk.CTkCanvas(app, bg="orange" ,height=55)
header_canvas.pack(fill="x")
# Create the main frame
main_canvas = ctk.CTkCanvas(app, bg='grey')
main_canvas.pack(expand=1, fill="both")

# Global Variables, a queue to store progress messages and a thread to run scans.
progress_queue = queue.Queue()
active_thread = None
#endregion
 
# Set up the log in info header and load the home page.
load_page("Home")
set_up_header(False)

#Ensure the program has all the required files and data
main_functions.check_for_creator_status_files()
main_functions.check_for_settings_file()
main_functions.populate_user_lists()

# Check the driver is operational and the steam API key is set
if(main_functions.start_driver() == False):
    load_page("Chrome Driver")
elif(main_functions.set_steam_api_key() == False):
    load_page("Add API Key")

app.mainloop()
