import xlsxwriter


txtFile = open("C:/Users/megaz/Documents/SteamWebScraper/Levels.txt", "r", encoding="utf-8")
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Levels.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Title')
worksheet.write('B1', 'Author Profile Link')
worksheet.write('C1', 'Author Name')
worksheet.write('D1', 'Detected Language')
worksheet.write('E1', 'Country')
worksheet.write('F1', 'Date Posted')
worksheet.write('G1', 'Tags')
worksheet.write('H1', 'Is Chinese?')

row = 1

for line in txtFile:
    if "Title:" in line:
        worksheet.write(row, 0, line.split(": ")[1])
    if "Author Profile Link:" in line:
        worksheet.write(row, 1, line.split(": ")[1])
    if "Author Name:" in line:
        worksheet.write(row, 2, line.split(": ")[1])
    if "Detected Language:" in line:
        worksheet.write(row, 3, line.split(": ")[1])
        if 'zh' in line.split(": ")[1]:
            worksheet.write(row, 7, "True")
        else:
            worksheet.write(row, 7, "False")
    if "Country" in line:
        worksheet.write(row, 4, line.split(": ")[1])
    if "Date Posted" in line:
        worksheet.write(row, 5, line.split(": ")[1].split(" ")[0])
    if "Tags" in line:
        worksheet.write(row, 6, line.split(": ")[1])
    if line == "\n":
        row += 1
workbook.close()
