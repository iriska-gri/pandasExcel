import numpy as np
import pandas as pd
import psycopg2 # Соединение с постгресс
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from openpyxl import load_workbook
from connectGoogle import ConnectGoogle



class WorkTest():
    def __init__(self):
        self.client = ConnectGoogle().connect()

    def settingssheet(self):
        file = {
            7: {

            }
        }

    def opengexcel(self):
        test = self.client.open('Тестовое задание для ТС')
        sheet_reports =test.get_worksheet(7)
        reports = pd.DataFrame(sheet_reports.get())
        
        # reports = reports.loc[2:]  
        # reports.columns = reports.iloc[0]
        # reports = reports.rename(columns=reports.iloc, axis=1).drop(reports.index) [0]
        print(reports)
        