from datetime import datetime
import xlsxwriter
import os
import main_functions
import tkinter as tk
import customtkinter as ctk
other_asian_language_codes = ['id', 'ja', 'ko', 'th', 'tl', 'vi']

def get_workshop_link(start_date, end_date):
    link = f"https://steamcommunity.com/workshop/browse/?appid=477160&searchtext=&childpublishedfileid=0&browsesort=mostrecent&section=readytouseitems&created_date_range_filter_start={start_date}&created_date_range_filter_end={end_date}&updated_date_range_filter_start=0&updated_date_range_filter_end=0&p=1"
    return link

def output_to_excel(start_date, end_date, workshop_data):
    start_date = datetime.fromtimestamp(start_date)
    end_date = datetime.fromtimestamp(end_date)
    workbook = xlsxwriter.Workbook(f'UGCChineseSpeakingCount{start_date.strftime("%m-%d-%Y")}_to_{end_date.strftime("%m-%d-%Y")}.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Date Posted')
    worksheet.write('B1', 'Title')
    worksheet.write('C1', 'Creator Name')
    worksheet.write('D1', 'Type')
    worksheet.write('E1', 'Country')
    worksheet.write('F1', 'Language')

    chineseLevels = 0
    chineseModels = 0
    otherAsianLevels = 0
    otherAsianModels = 0
    totalLevels = 0
    totalModels = 0
    for(i, item) in enumerate(workshop_data):
        worksheet.write(i+1, 0, item.date_posted)
        worksheet.write(i+1, 1, item.title)
        worksheet.write(i+1, 2, item.creator_name)
        worksheet.write(i+1, 3, item.item_type)
        worksheet.write(i+1, 4, item.country)
        worksheet.write(i+1, 5, item.language)
        if 'zh' in item.language:
            if item.item_type == 'Level':
                chineseLevels += 1
            elif item.item_type == 'Model':
                chineseModels += 1
        elif item.language in other_asian_language_codes:
            if item.item_type == 'Level':
                otherAsianLevels += 1
            elif item.item_type == 'Model':
                otherAsianModels += 1
        if item.item_type == 'Level':
            totalLevels += 1
        elif item.item_type == 'Model':
            totalModels += 1
    worksheet.write('H2', 'Models')
    worksheet.write('H3', 'Chinese Entries')
    worksheet.write('H4', 'Other Asian Entries')
    worksheet.write('H5', 'Non-Asian Entries')

    worksheet.write('H7', 'Levels')
    worksheet.write('H8', 'Chinese Entries')
    worksheet.write('H9', 'Other Asian Entries')
    worksheet.write('H10', 'Non-Asian Entries')

    worksheet.write('H12', 'Total')
    worksheet.write('H13', 'Chinese Entries')
    worksheet.write('H14', 'Other Asian Entries')
    worksheet.write('H15', 'Non-Asian Entries')
    def percentage(part, whole):
        try:
            return part/whole
        except ZeroDivisionError:
            return 0

    worksheet.write('I2', totalModels)
    worksheet.write('I3', f"{chineseModels}")
    worksheet.write('J3', f"{percentage(chineseModels, totalModels):.2%}")
    worksheet.write('I4', f"{otherAsianModels}")
    worksheet.write('J4', f"{percentage(otherAsianModels, totalModels):.2%}")
    nonAsianModels = totalModels - chineseModels - otherAsianModels
    worksheet.write('I5', f"{nonAsianModels}")
    worksheet.write('J5', f"{percentage(nonAsianModels, totalModels):.2%}")

    worksheet.write('I7', totalLevels)
    worksheet.write('I8', f"{chineseLevels}")
    worksheet.write('J8', f"{percentage(chineseLevels, totalLevels):.2%}")
    worksheet.write('I9', f"{otherAsianLevels}")
    worksheet.write('J9', f"{percentage(otherAsianLevels, totalLevels):.2%}")
    nonAsianLevels = totalLevels - chineseLevels - otherAsianLevels
    worksheet.write('I10', f"{nonAsianLevels}")
    worksheet.write('J10', f"{percentage(nonAsianLevels,totalLevels):.2%}")

    worksheet.write('I12', totalLevels + totalModels)
    worksheet.write('I13', f"{chineseLevels + chineseModels}")
    worksheet.write('J13', f"{percentage(chineseLevels + chineseModels, totalLevels + totalModels):.2%}")
    worksheet.write('I14', f"{otherAsianLevels + otherAsianModels}")    
    worksheet.write('J14', f"{percentage(otherAsianLevels + otherAsianModels, totalLevels + totalModels):.2%}")
    nonAsianEntries = nonAsianLevels + nonAsianModels
    worksheet.write('I15', f"{nonAsianEntries}")
    worksheet.write('J15', f"{percentage(nonAsianEntries, totalLevels + totalModels):.2%}")

    workbook.close() 
    os.startfile(f'UGCChineseSpeakingCount{start_date.strftime("%m-%d-%Y")}_to_{end_date.strftime("%m-%d-%Y")}.xlsx')

def scan(start_date, end_date, footer_label):
    link = get_workshop_link(start_date, end_date)
    footer_label.pack()
    footer_label.configure(text="Loading workshop page...")
    main_functions.driver.get(link)
    footer_label.configure(text="Getting item IDs...")
    item_ids = main_functions.get_item_ids()
    footer_label.configure(text="Creating workshop data...")
    workshop_data = []
    for i in range(len(item_ids)):
        footer_label.configure(text=f"Gathering workshop data for item {i+1} of {len(item_ids)}")
        workshop_data.append(main_functions.create_workshop_item(item_ids[i]))
    footer_label.configure(text="Outputting to Excel...")
    output_to_excel(start_date, end_date, workshop_data)
    footer_label.configure(text="")
