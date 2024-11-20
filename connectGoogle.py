import gspread
from oauth2client.service_account import ServiceAccountCredentials

class ConnectGoogle():
    def __init__(self):
        pass

    def connect(self):
        pass
        # scope = ['https://www.googleapis.com/auth/spreadsheets',
        # "https://www.googleapis.com/auth/drive"]

        # credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
        # client = gspread.authorize(credentials)
        # return client