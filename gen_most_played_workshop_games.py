from datetime import date
import xlsxwriter
import main_functions
import os
def output_to_excel(games):
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
    os.startfile('UGCOfMajorGames.xlsx')

def scan(progress_queue):
    progress_queue.put("Getting current top 100 games from SteamDB...")
    appIDs = main_functions.get_top_100_appIDs_steamDB() 
    progress_queue.put("Creating game items...")
    games = []
    for i in range(len(appIDs)):
        progress_queue.put(f"Gathering workshop data for game {i+1} of {len(appIDs)}")
        games.append(main_functions.create_game_item(appIDs[i]))    
    progress_queue.put("Outputting to Excel...")
    output_to_excel(games)
    progress_queue.put("")
