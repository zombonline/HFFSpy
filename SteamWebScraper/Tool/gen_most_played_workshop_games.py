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

def scan():
    appIDs = main_functions.get_top_100_games_via_steamDB() 
    games = main_functions.create_game_items(appIDs)
    output_to_excel(games)
