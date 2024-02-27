import tkinter as tk
import customtkinter as ctk
app = ctk.CTk()
app.title("Curve Games Tool")
app.geometry('1280x720')
games = ["League of Legends", "Fortnite", "Apex Legends", "Overwatch", "CS:GO", "Dota 2", "PUBG", "Hearthstone", "Rainbow Six Siege", "Rocket League", "Smite", "Paladins", "Warframe", "World of Tanks", "World of Warships", "World of Warplanes", "Crossout", "Armored Warfare", "Star Conflict", "Trove", "Skyforge", "Neverwinter", "TERA", "Aion", "Lineage II", "Blade & Soul", "Guild Wars 2", "Rift", "ArcheAge", "Defiance 2050", "Defiance", "Atlas Reactor"]
def load_home_page():
    clear_window()
    title = ctk.CTkLabel(app, text="Welcome!", font=("Arial", 20))
    title.pack(padx=10, pady=10)    

    button = ctk.CTkButton(app, text="Generate UGC Count Of Major Games!", width=100, height=2, command=lambda: load_cool_page())  
    button.pack(padx=10, pady=10)

    

    button2 = ctk.CTkButton(app, text="Click me!", width=10, height=2)
    button2.pack(padx=10, pady=10)

def load_cool_page():
    clear_window()
    title = ctk.CTkLabel(app, text="Cool page!", font=("Arial", 20))
    title.pack(padx=10, pady=10)    

    button = ctk.CTkButton(app, text="Home", width=100, height=2, command=lambda: load_home_page())  
    button.pack(padx=10, pady=10)
    
    info = ctk.CTkLabel(app, text="Scanning will yield results for the following games: \n")
    info.pack(padx=10, pady=10)

    for game in games:
        game_label = ctk.CTkLabel(app, text=game)
        game_label.pack()

    button2 = ctk.CTkButton(app, text="Click me!", width=10, height=2)
    button2.pack(padx=10, pady=10)

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

load_home_page()
app.mainloop()