import tkinter as tk
import customtkinter as ctk
import os
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
def load_page(page):
    for widget in main_frame.winfo_children():
        widget.destroy()
    if page == "Home":
        set_up_home_page()
    elif page == "Total UGC Count":
        set_up_total_UGC_count_page()
    else:
        print("Error: Page not found")

#region input elements
add_appID_input = tk.StringVar()
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
#endregion

load_page("Home")

app.mainloop()


