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
                'settings': {
                    'static': {
                            "кластер" : [3, 1],
                            "Код мониторинга" : [3, 0],
                            'Название города' : [13, 1],
                            'Конкурент': [14, 0]
                        },
                    'renames': {
                        'SAP код товара':'Артикул Метро',
                        'Код товара':'Артикул МГБ',
                        'Наименование товара':'Название артикула',
                        'Примечания для мониторинга':'Описание'
                    },
                },
                'sheet' : [7, 8]
        }

        
        df = pd.DataFrame()
        for val in file['sheet']:
            df = pd.concat([df, self.opengexcel(val, file['settings'])])
            # print(val)
            # for val in key['sheet']:
        
        # for [file, settings] in file.items():
        #     # df =  self.opengexcel(file, settings)
         
        #     df= pd.concat([df, self.opengexcel(file, settings)])
        print(df)

        


    def opengexcel(self, file, settings):
        test = self.client.open('Тестовое задание для ТС')

        sheet_reports =test.get_worksheet(file)
        reports = pd.DataFrame(sheet_reports.get())
        
        newreports = reports.loc[2:] 
        
        df1 = newreports.rename(columns=newreports.iloc[0])
        df1.drop(2 ,axis=0, inplace= True)
        df1.rename(columns= settings['renames'], inplace=True)
        # print(df1)
        # df1 = df1[[]]
        # # # print(newreports)

        # for [key, val] in settings['static'].items():
        #     df1.insert(loc = 0,  # это будет второй по счёту столбец
        #     column = key,
        #     value = reports[val[0]].loc[reports.index[val[1]]])  # название столбца
        # print(newreports)
        # print(reports[['Код мониторинга']])
        return df1     
            # reports = pd.DataFrame(sheet_reports.get())
            
        
        # reports = reports.loc[2:]  
        # reports.columns = reports.iloc[0]
        # reports = reports.rename(columns=reports.iloc, axis=1).drop(reports.index) [0]

        # 
   
        