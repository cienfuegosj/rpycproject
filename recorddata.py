import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread.json', scope)
gc = gspread.authorize(credentials)
sh = gc.create('Test Sheet')
sh.share('cienfuegoseveryday@gmail.com', perm_type='user', role='writer')
worksheet = sh.get_worksheet(0)
cell_list = worksheet.range('A1:C7')
for cell in cell_list:
    cell.value = cell.row()
