import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread.json', scope)
gc = gspread.authorize(credentials)
sh = gc.create('Test Sheet')
sh.share('cienfuegoseveryday@gmail.com', perm_type='user', role='writer')
worksheet = sh.get_worksheet(0)
celllist = worksheet.range('A1:A100')
for cell in celllist:
	cell.value = '0'
worksheet.update_cells(celllist)
