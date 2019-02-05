import xlrd

# Location of the file
loc = 'Excel 1.xlsx'

# To open workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
