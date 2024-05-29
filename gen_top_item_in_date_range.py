from datetime import date
import xlsxwriter
import main_functions
import os
import queue
def output_to_excel(level_list, model_list):
    
    workbook = xlsxwriter.Workbook('UGCOfWorkshopMonth.xlsx')
    worksheet = workbook.add_worksheet()
    format_dict = {
        "Signed": workbook.add_format({'bold': True, 'bg_color': 'green'}),
        "Contacted": workbook.add_format({'bold': True, 'bg_color': 'yellow'}),
        "Planned": workbook.add_format({'bold': True, 'bg_color': 'red'}),
        None: workbook.add_format({'bold': False, 'bg_color': 'white'})
    }

    worksheet.write('K1', "Key")
    worksheet.write('K2', "Signed", format_dict["Signed"])
    worksheet.write('K3', "Contacted", format_dict["Contacted"])
    worksheet.write('K4', "Planned", format_dict["Planned"])

    worksheet.write('A1', 'Level')
    worksheet.write('A2', 'Rank')
    worksheet.write('B2', 'Title')
    worksheet.write('C2', 'Creator')
    worksheet.write('D2', 'Date Posted')
    worksheet.write('E2', 'Country')
    worksheet.write('F2', 'Language')
    worksheet.write('G2', f'TUS ({date.today()})')
    worksheet.write('H2', 'Rating')
    worksheet.write('I2', 'Comment Count')

    nextHeaderCount = 4 + len(level_list)
    worksheet.write('A' + str(nextHeaderCount-1), 'Model')
    worksheet.write('A' + str(nextHeaderCount), 'Rank')
    worksheet.write('B' + str(nextHeaderCount), 'Title')
    worksheet.write('C' + str(nextHeaderCount), 'Creator')
    worksheet.write('D' + str(nextHeaderCount), 'Date Posted')
    worksheet.write('E' + str(nextHeaderCount), 'Country')
    worksheet.write('F' + str(nextHeaderCount), 'Language')
    worksheet.write('G' + str(nextHeaderCount), f'TUS ({date.today()})')
    worksheet.write('H' + str(nextHeaderCount), 'Rating')
    worksheet.write('I' + str(nextHeaderCount), 'Comment Count')

    for i in range(len(level_list)):
        worksheet.write(i+2, 0, i+1)
        worksheet.write(i+2, 1, level_list[i].title)
        worksheet.write(i+2, 2, level_list[i].creator_name, format_dict[level_list[i].creator_status])
        worksheet.write(i+2, 3, level_list[i].date_posted)
        worksheet.write(i+2, 4, level_list[i].country)
        worksheet.write(i+2, 5, level_list[i].language)
        worksheet.write(i+2, 6, level_list[i].tus)
        worksheet.write(i+2, 7, level_list[i].rating)
        worksheet.write(i+2, 8, level_list[i].comment_count)
    for i in range(len(model_list)):
        worksheet.write(i + nextHeaderCount, 0, i+1)
        worksheet.write(i + nextHeaderCount, 1, model_list[i].title)
        worksheet.write(i + nextHeaderCount, 2, model_list[i].creator_name, format_dict[model_list[i].creator_status])
        worksheet.write(i + nextHeaderCount, 3, model_list[i].date_posted)
        worksheet.write(i + nextHeaderCount, 4, model_list[i].country)
        worksheet.write(i + nextHeaderCount, 5, model_list[i].language)
        worksheet.write(i + nextHeaderCount, 6, model_list[i].tus)
        worksheet.write(i + nextHeaderCount, 7, model_list[i].rating)
        worksheet.write(i + nextHeaderCount, 8, model_list[i].comment_count)
    workbook.close() 
    os.startfile('UGCOfWorkshopMonth.xlsx')

def scan(start_date_timestamp, end_date_timestamp, amount_of_items, progress_queue):
    progress_queue.put("Loading workshop levels page...")
    level_link = f"https://steamcommunity.com/workshop/browse/?appid=477160&browsesort=trend&section=readytouseitems&requiredtags%5B0%5D=Levels&created_date_range_filter_start={start_date_timestamp}&created_date_range_filter_end={end_date_timestamp}&updated_date_range_filter_start=NaN&updated_date_range_filter_end=NaN&actualsort=trend&p=1"
    main_functions.driver.get(level_link)
    progress_queue.put("Getting level item IDs...")
    item_ids = main_functions.get_item_ids(amount_of_items)
    level_workshop_data = []
    for i in range(len(item_ids)):
        progress_queue.put(f"Gathering workshop data for level {i+1} of {len(item_ids)}")
        level_workshop_data.append(main_functions.create_workshop_item(item_ids[i]))

    progress_queue.put("Loading workshop models page...")
    model_link = f"https://steamcommunity.com/workshop/browse/?appid=477160&browsesort=trend&section=readytouseitems&requiredtags%5B0%5D=Model&created_date_range_filter_start={start_date_timestamp}&created_date_range_filter_end={end_date_timestamp}&updated_date_range_filter_start=NaN&updated_date_range_filter_end=NaN&actualsort=trend&p=1"
    main_functions.driver.get(model_link)
    progress_queue.put("Getting model item IDs...")
    item_ids = main_functions.get_item_ids(amount_of_items)
    model_workshop_data = []
    for i in range(len(item_ids)):
        progress_queue.put(f"Gathering workshop data for model {i+1} of {len(item_ids)}")
        model_workshop_data.append(main_functions.create_workshop_item(item_ids[i]))
    
    progress_queue.put("Outputting to Excel...")
    output_to_excel(level_workshop_data, model_workshop_data)
    progress_queue.put("")