import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/']

credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread.json', scope)
