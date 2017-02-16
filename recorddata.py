import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread.json', scope)
gc = gspread.authorize(credentials)

#sh = gc.create('Testing Spreadsheet')
#sh.share('cienfuegoseveryday@gmail.com', perm_type='user', role='owner')
for spreadsheet in gc.openall():
  gc.insert_permission(
    spreadsheet.id,
    None,
    perm_type='anyone',
    role='writer'
  )
  
for spreasheet in gc.openall():
  gc.del_spreadsheet(spreadsheet.id)

  
  
 