from datetime import date
import xlsxwriter
import main_functions
import os


def output_to_excel(data_lists, excel_outputs):
    workbook = xlsxwriter.Workbook('UGCOfWorkshopMonth.xlsx')
    format_dict = {
        "Signed": workbook.add_format({'bold': True, 'bg_color': 'green'}),
        "Contacted": workbook.add_format({'bold': True, 'bg_color': 'yellow'}),
        "Planned": workbook.add_format({'bold': True, 'bg_color': 'orange'}),
        None: workbook.add_format({'bold': False, 'bg_color': 'white'})
    }
    other_asian_language_codes = ['id', 'ja', 'ko', 'th', 'tl', 'vi']
    chinese_levels = 0
    chinese_models = 0
    other_asian_levels = 0
    other_asian_models = 0
    total_levels = 0
    total_models = 0

    for list in data_lists:
        if len(data_lists) > 1:
            worksheet = workbook.add_worksheet(list[0].item_type)
        else:
            worksheet = workbook.add_worksheet('UGCOfWorkshopMonth')
        worksheet.write(0,0,'Rank')
        col = 1
        for item in excel_outputs:
            if excel_outputs[item][1]:
                worksheet.write(0,col,item)
                col+=1
        col+=1

        worksheet.write(0,col,'Creator Status Key')
        worksheet.write(1,col,'Signed', format_dict["Signed"])
        worksheet.write(2,col,'Contacted', format_dict["Contacted"])
        worksheet.write(3,col,'Planned', format_dict["Planned"])
        col+=1

        language_listed = excel_outputs['Language'][1]
        if language_listed:
            worksheet.write(0, col, 'Asian Entries')
            worksheet.write(1, col, 'Chinese Levels')
            worksheet.write(2, col, 'Other Asian Levels')
            worksheet.write(3, col, 'Non-Asian Levels')
            worksheet.write(5, col, 'Chinese Models')
            worksheet.write(6, col, 'Other Asian Models')
            worksheet.write(7, col, 'Non-Asian Models')
            worksheet.write(9, col, 'Chinese Total')
            worksheet.write(10, col, 'Other Asian Total')
            worksheet.write(11, col, 'Non-Asian Total')

        chinese_results_col = col+1

        row = 1
        for workshop_item in list:
            # Counting the number of Chinese and other Asian entries
            if workshop_item.item_type == 'Level':
                total_levels += 1
                if 'zh' in workshop_item.language:
                    chinese_levels += 1
                elif workshop_item.language in other_asian_language_codes:
                    other_asian_levels += 1
            elif workshop_item.item_type == 'Model':
                total_models += 1
                if 'zh' in workshop_item.language:
                    chinese_models += 1
                elif workshop_item.language in other_asian_language_codes:
                    other_asian_models += 1
            # Rank on far left column
            worksheet.write(row,0,row)
            col = 1
            # Write data of the item.
            for item in excel_outputs:
                if excel_outputs[item][1]:
                    worksheet.write(row,col,getattr(workshop_item, excel_outputs[item][0]))
                    col+=1
            row += 1

        if language_listed:
            non_asian_levels = total_levels - chinese_levels - other_asian_levels
            non_asian_models = total_models - chinese_models - other_asian_models

            #region get percentages
            try:
                chinese_level_percentage = chinese_levels / total_levels
            except ZeroDivisionError:
                chinese_level_percentage = 0
            try:
                chinese_model_percentage = chinese_models / total_models
            except ZeroDivisionError:
                chinese_model_percentage = 0
            try: 
                chinese_total_percentage = (chinese_levels + chinese_models) / (total_levels + total_models)
            except ZeroDivisionError:
                chinese_total_percentage = 0
            try:
                other_asian_level_percentage = other_asian_levels / total_levels
            except ZeroDivisionError:
                other_asian_level_percentage = 0
            try:
                other_asian_model_percentage = other_asian_models / total_models
            except ZeroDivisionError:
                other_asian_model_percentage = 0
            try:
                other_asian_total_percentage = (other_asian_levels + other_asian_models) / (total_levels + total_models)
            except ZeroDivisionError:
                other_asian_total_percentage = 0
            try:
                non_asian_level_percentage = non_asian_levels / total_levels
            except ZeroDivisionError:
                non_asian_level_percentage = 0
            try:
                non_asian_model_percentage = non_asian_models / total_models
            except ZeroDivisionError:
                non_asian_model_percentage = 0
            try:
                non_asian_total_percentage = (non_asian_levels + non_asian_models) / (total_levels + total_models)
            except ZeroDivisionError:
                non_asian_total_percentage = 0
            #endregion
        
            worksheet.write(1, chinese_results_col, f"{chinese_level_percentage:.2%}")
            worksheet.write(2, chinese_results_col, f"{other_asian_level_percentage:.2%}")
            worksheet.write(3, chinese_results_col, f"{non_asian_level_percentage:.2%}")
            worksheet.write(5, chinese_results_col, f"{chinese_model_percentage:.2%}")
            worksheet.write(6, chinese_results_col, f"{other_asian_model_percentage:.2%}")
            worksheet.write(7, chinese_results_col, f"{non_asian_model_percentage:.2%}")
            worksheet.write(9, chinese_results_col, f"{chinese_total_percentage:.2%}")
            worksheet.write(10, chinese_results_col, f"{other_asian_total_percentage:.2%}")
            worksheet.write(11, chinese_results_col, f"{non_asian_total_percentage:.2%}")
            

    workbook.close()
    os.startfile('UGCOfWorkshopMonth.xlsx')        

def scan(start_date_timestamp, end_date_timestamp, amount_of_items, sort_by, seperate_levels_and_models, excel_outputs, progress_queue):
    
    print("Start Date: ", start_date_timestamp)
    print("End Date: ", end_date_timestamp)
    print("Amount of Items: ", amount_of_items)
    print("Sort By: ", sort_by)
    print("Seperate Levels and Models: ", seperate_levels_and_models)
    print("Excel Outputs: ", excel_outputs)
    progress_queue.put("Loading workshop levels page...")
    if sort_by == "Most Popular":
        sort_by = "trend"
    elif sort_by == "Most Recent":
        sort_by = "mostrecent"

    if seperate_levels_and_models:
        level_link = f"https://steamcommunity.com/workshop/browse/?appid=477160&browsesort={sort_by}&section=readytouseitems&requiredtags%5B0%5D=Levels&created_date_range_filter_start={start_date_timestamp}&created_date_range_filter_end={end_date_timestamp}&updated_date_range_filter_start=NaN&updated_date_range_filter_end=NaN&actualsort={sort_by}&p=1"
        main_functions.driver.get(level_link)
        progress_queue.put("Getting level item IDs...")
        item_ids = main_functions.get_item_ids(amount_of_items)
        level_workshop_data = []
        for i in range(len(item_ids)):
            progress_queue.put(f"Gathering workshop data for level {i+1} of {len(item_ids)}")
            item = main_functions.create_workshop_item(item_ids[i], excel_outputs)
            if item is None:
                print(f"No data retreieved for item {i+1} of {len(item_ids)}, id: {item_ids[i]}")
                continue
            level_workshop_data.append(item)

        progress_queue.put("Loading workshop models page...")
        model_link = f"https://steamcommunity.com/workshop/browse/?appid=477160&browsesort={sort_by}&section=readytouseitems&requiredtags%5B0%5D=Model&created_date_range_filter_start={start_date_timestamp}&created_date_range_filter_end={end_date_timestamp}&updated_date_range_filter_start=NaN&updated_date_range_filter_end=NaN&actualsort={sort_by}&p=1"
        main_functions.driver.get(model_link)
        progress_queue.put("Getting model item IDs...")
        item_ids = main_functions.get_item_ids(amount_of_items)
        model_workshop_data = []
        for i in range(len(item_ids)):
            progress_queue.put(f"Gathering workshop data for model {i+1} of {len(item_ids)}")
            item = main_functions.create_workshop_item(item_ids[i],excel_outputs)
            if item is None:
                print(f"No data retreieved for item {i+1} of {len(item_ids)}, id: {item_ids[i]}")
                continue
            model_workshop_data.append(item)
        progress_queue.put("Outputting to Excel...")
        data_lists = [level_workshop_data, model_workshop_data]
        output_to_excel(data_lists, excel_outputs)
    else:
        link = f"https://steamcommunity.com/workshop/browse/?appid=477160&browsesort={sort_by}&section=readytouseitems&created_date_range_filter_start={start_date_timestamp}&created_date_range_filter_end={end_date_timestamp}&updated_date_range_filter_start=NaN&updated_date_range_filter_end=NaN&actualsort={sort_by}&p=1"
        main_functions.driver.get(link)
        progress_queue.put("Getting item IDs...")
        item_ids = main_functions.get_item_ids(amount_of_items) 
        workshop_data = []
        for i in range(len(item_ids)):
            progress_queue.put(f"Gathering workshop data for item {i+1} of {len(item_ids)}")
            item = main_functions.create_workshop_item(item_ids[i], excel_outputs)
            if item is None:
                print(f"No data retreieved for item {i+1} of {len(item_ids)}, id: {item_ids[i]}")
                continue
            workshop_data.append(item)
        progress_queue.put("Outputting to Excel...")
        data_lists = [workshop_data]
        output_to_excel(data_lists, excel_outputs)
    progress_queue.put("")