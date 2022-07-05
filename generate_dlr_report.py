import requests
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
import pytz
from datetime import datetime

result = requests.get('https://app.buildahome.in/erp/get_dlr_report')
rb = open_workbook("static/updates.xls")
wb = copy(rb)
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST)
current_time = current_time.strftime('%d-%m-%Y')
ws = wb.add_sheet(' ' + str(current_time))
style = xlwt.XFStyle()

# font
font = xlwt.Font()
font.bold = True
style.font = font


yellow_style = xlwt.XFStyle()
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = xlwt.Style.colour_map['yellow']
yellow_style.pattern = pattern

ws.write(1, 0, 'Project name', style=style)
ws.write(1, 1, 'Project number', style=style)
ws.write(1, 2, 'Update', style=style)
ws.write(1, 3, 'Workman status', style=style)

row = 2
column = 0
read_only = xlwt.easyxf("")

data_from_url = result.json()
for project_data in data_from_url:
    column = 0
    ws.col(column).width = 8000
    ws.write(row, column, project_data['project_name'], read_only)

    column = column + 1
    ws.col(column).width = 8000
    ws.write(row, column, project_data['project_number'], read_only)

    column = column + 1
    ws.col(column).width = 15000
    if project_data['update'] == 'DLR not updated':
        ws.write(row, column, project_data['update'], style=yellow_style)
    else:
        ws.write(row, column, project_data['update'], read_only)

    column = column + 1
    ws.col(column).width = 10000
    if len(project_data['workman_status'].strip()) > 0:
        project_data['workman_status'] = project_data['workman_status'][1:-1]
    ws.write(row, column, project_data['workman_status'], read_only)

    row = row + 1

wb.save('static/updates.xls')