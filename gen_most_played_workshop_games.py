from datetime import datetime
import xlsxwriter
import main_functions
import os
from pathlib import Path
def output_to_excel(games):
    dt = datetime.now()
    documents_path = Path(os.path.expanduser('~')) / 'Documents'
    sheets_path = documents_path / 'HFFSpy Sheets'
    if not sheets_path.exists():
        sheets_path.mkdir()

    filename = f'Steam top 100 Scan {dt.year}-{dt.month}-{dt.day}-{dt.hour}-{dt.minute}-{dt.second}.xlsx'
    full_path = sheets_path / filename

    workbook = xlsxwriter.Workbook(full_path)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Rank')
    worksheet.write('B1', 'Game Name')
    worksheet.write('C1', f'Amount of Workshop Items as of {datetime.today().date()}')

    for i in range(len(games)):
        worksheet.write(i+1, 0, i+1)
        worksheet.write(i+1, 1, games[i].name)
        worksheet.write(i+1, 2, games[i].amountOfItems)
    
    workbook.close()
    os.startfile(full_path)

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

