import numpy as np
import pandas as pd
import psycopg2 # Соединение с постгресс
import psycopg2.extras as extras 
from sqlalchemy import create_engine
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from openpyxl import load_workbook
from connectGoogle import ConnectGoogle
from sqlalchemy import create_engine 
import csv
import io
# from oauth2client.service_account import ServiceAccountCredentials

class Connect():


    def __init__(self):
        try:
            self.conn = psycopg2.connect(dbname='pandas', user='postgres', password='admin', host='127.0.0.1')
            # Создаем подключение к бд
            self.cur = self.conn.cursor()
            print('Соединен с БД')
          

        except:
            # в случае сбоя подключения будет выведено сообщение в STDOUT
            print('Can`t establish connection to database')
    

    # создать таблицу 
    def nameTable(self,name, mass):
                         
        query = f"CREATE TABLE IF NOT EXISTS {name} ({self.dictparser(mass)})" 
        self.cur.execute(query)
        self.conn.commit() 
        # print(query)

    def selectTable(self):
        df = pd.read_sql_query('select * from "test"',con=self.conn)
      
        print(df)
        # query= "SELECT * FROM test"
       
        # # query = f"INSERT INTO test (names, age) VALUES ('Jon', '8')"
        # self.cur.execute(query)
        # self.conn.commit() 
        # print(self.conn)
  
    # def insertTable(self):
    #     query = "INSERT INTO questionnaire1 (groups, category, subcategory, epp, ctm, cargo_code, sub_cargo_code, schrih_code, product_name, need, monitoring_note, regular_price, promotional_price, name_promotion) VALUES ('СОФ', 'P0', '15.Овощи', '1501', '150101', '1', '0', '150101162743', '162743', '2099999731574, 2462743000000', 'Огурцы среднеплодные гладкие вес ()', 'X', 'EPP_KVI, средние гладкие, цена за кг', 'd')"
    #     self.cur.execute(query)
    #     self.conn.commit() 
#         headers = ['groups', 'category', 'subcategory', 'epp', 'ctm', 'cargo_code', 'sub_cargo_code', 'schrih_code', 
	# 'product_name', 'need', 'monitoring_note', 'regular_price', 'promotional_price', 'name_promotion']
    def insertInto(self, df):
        # query= "SELECT * FROM test"
        
        query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'anketa' ORDER BY ordinal_position ASC"
        g = pd.read_sql(query, self.conn)
        self.cur.execute(query)
        self.conn.commit() 
        postcolmn = g['column_name'].to_list()
        postcolmn.remove('id')
        res = {list(df)[i]: postcolmn[i] for i in range(len(list(df)))}

       
        df = df.rename(columns=res)
    
        engine = create_engine('postgresql://postgres:admin@localhost:5432/pandas')
        df.to_sql(
            name="anketa", # имя таблицы
            con=engine,  # движок
            if_exists="append", # если таблица уже существует, добавляем
            index=False # без индекса
        )
       

    def dictparser(self, mass):
        lists = []
        for [key, val] in mass.items(): 
            lists.append( f"{key} {val}")
        
        return ", ".join(lists)
            

    def diconect(self):
        self.conn.close()
        print('Разъеденение')



class UploadCSV():

    def __init__(self, message='привет') -> None:
        self.message=message
        self.connection = Connect()

        pass

    def newdate(self, row):
        text = f"Сплошной сбор по категориям ({datetime.datetime.strftime(row['старт'],'%d.%m')}-{datetime.datetime.strftime(row['финиш'],'%d.%m')}) "
        return text

    def pro(self):
        self.connection.insertInto()
            # data = {'name': ['Tom', 'dick', 'harry'], 
            #         'age': [22, 21, 24]} 
            
            # # Create DataFrame 
            # df = pd.DataFrame(data) 
            # tuples = [tuple(x) for x in df.to_numpy()] 
            # cols = ','.join(list(df.columns)) 
            # query = "INSERT INTO %s(%s) VALUES %%s" % ('test', cols) 
            # self.cur.execute(query)
            # self.conn.commit() 
            # print(cols)
           
       
  
# conn.commit() 
   
       

    def crossjoin(self):
       
        # сохраняем файлы для чтения
        df1 = pd.read_excel('код.xlsx')
        df2 = pd.read_excel('Задания.xlsx')

        df1['key1'] = 0
        df2['key1'] = 0

        # Объеденям таблицы
        df = df1.merge(df2, on='key1', how='right')
        # Добавляем необходимые колонки вместе с пустыми
        df['старт'] = df['Дата отчета'].apply(lambda x:  x - datetime.timedelta(days=10))
        df['финиш'] = df['Дата отчета'].apply(lambda x: x - datetime.timedelta(days=3))
        for i in range(2,6):
            df[f"уровень {i}"] = ''
        df['подгруппа 1'] = df.apply(self.newdate, axis = 1)
        # Преобразуем формат
        df['старт'] =  df['старт'].apply(lambda x:  datetime.datetime.strftime(x,'%d.%m.%Y'))
        df['финиш'] =  df['финиш'].apply(lambda x:  datetime.datetime.strftime(x,'%d.%m.%Y'))
        df['подгруппа2'] = df['Группировка']
        df['волна'] = ''
        # Удаляем ненужные столбцы
        df= df.drop(columns=['key1', 'Конкурент','Дата отчета', 'Группировка'])
        # Переименовываем столбцы
        df = df.rename(columns={'id': 'id ат', 'Задание': 'категория (название задания)', 'Описание': 'описание задания'})
        # Сохраняем в Excel
        df.to_excel('задание 4.xlsx', index=False)
        print('Создано')
       


    def circleexcel(self):
        file= {
            'A1.xlsx': {
                'ws': {
                    "Код мониторинга": 'B1',
                     "кластер":'B2',
                     "Название города": 'N2',
                     "Конкурент":'M1'
                },
                'renames': {
                    'SAP код товара':'Артикул Метро',
                    'Код товара':'Артикул МГБ',
                    'Наименование товара':'Название артикула',
                    'Примечания для мониторинга':'Описание',
                    'Группа текущая (код и название)':'Категория'
                },
                'dropcolumn':  ["EPP", "Категория", "ЧТМ", "Штрих-код товара", "Признак необходимости фотоконтроля", "Регулярная цена", "Акционная цена", "Примечание, название акции", 'Подкатегория']
            },
            'A2.xlsx': {
                'ws': {
                    "Код мониторинга": 'D1',
                     "кластер":'D2',
                     "Название города": 'O2',
                     "Конкурент":'O1'
                },
                'renames': {
                    'SAP код товара':'Артикул Метро',
                    'Код товара':'Артикул МГБ',
                    'Наименование товара':'Название артикула',
                    'Примечания для мониторинга':'Описание',
                    'Группа текущая (код и название)':'Категория'
                },
                'dropcolumn':  ["Подтип мониторинга", "ГЗ","Категория", "Подкатегория", "EPP", "ЧТМ", "Штрих-код товара", "Признак необходимости фотоконтроля", "Регулярная цена", "Акционная цена"]
            }
        }

        # Создаем DataFrame и перебираем данные с названием файла и настройками для него
        df = pd.DataFrame()
        for [file, settings] in file.items():
            # Объединяем два файла
            df = pd.concat([df, self.openexcel(file, settings)])

        #  Сохраняем строкой колонку чтобы был читабельный вид при открытии excel
        df['Артикул МГБ'] = df['Артикул МГБ'].astype('string')


        # df.to_excel('данные.xlsx', index=False)
        # print(df)

    def  wsiterator(self, sheet, settingws):
        newdict = {}
        for [key, val] in settingws.items():
            newdict[key] = sheet[val].value
        return newdict

    def openexcel(self, file, settings):
        # читаем файл 
        re = pd.read_excel(file, header=2)
        # загружаем лист для доступа к ячейкам
        wb = load_workbook(file)
        ws = wb.active
    
    # создание колонок с ключом empty будут пустые данные с функцией wsiterator передаем лист и настройки, для заполнения данных
        newcolumn =  {
            'empty':  ["Код города", "Название артикула_site", "Бренд", "Метод сбора", "Единица измерения цены Мetro", "Вес Метро","Вид упаковки","Страна","Код конкурента","Подкатегория"],
            **self.wsiterator(ws, settings['ws'])
        }

# удаляем колонки описанные в настройках
        re.drop(columns=settings['dropcolumn'])
        # переименовываем колонки согласно настройкам
        re.rename(columns= settings['renames'], inplace=True)

        # перебирем словарь для заполнения данных
        for [key, val] in newcolumn.items():
            
            if key == "empty" :
                for x in val:
                        re[x] = ''
            else:
                re[key] = val

#   Сортировка столбцов
        re = re[["Код мониторинга", "кластер", "Код города", "Название города", "Артикул Метро", "Артикул МГБ",
                           "Название артикула", "Название артикула_site", "Бренд", "Метод сбора",
                           "Описание", "Единица измерения цены Мetro", "Вес Метро", "Вид упаковки", "Страна", "Код конкурента", "Конкурент", "Категория", "Подкатегория"
                           ]]
        # print(re)
  
        return re

          


    def uploadexcel(self):
            try:
                client = ConnectGoogle().connect()
                test = client.open('Тестовое задание для ТС')
                sheet_reports =test.get_worksheet(2)
                reports = pd.DataFrame(sheet_reports.get_all_records(), columns=['user_id', 'geo_object_id', 'report_state'])
                j =  reports.groupby(['user_id', 'geo_object_id'])['report_state'].count().to_frame(name='count')
                
                l = reports.loc[reports['report_state'] == 'accepted']

                lamd = l.groupby(['user_id', 'geo_object_id'])['report_state'].count().to_frame(name='accepted')
                j = j.merge(lamd, left_on=['user_id', 'geo_object_id'], right_on=['user_id', 'geo_object_id'])
               
                unicreports = reports[['user_id', 'geo_object_id']].drop_duplicates()

              
                unicreports = unicreports.merge(j, left_on=['user_id', 'geo_object_id'], right_on=['user_id', 'geo_object_id'])
                # unicreports = unicreports.merge(j, left_on=['user_id', 'geo_object_id'], right_on=['user_id', 'geo_object_id'])
                
                sheet_reports =test.get_worksheet(4)
                users = pd.DataFrame(sheet_reports.get_all_records(), columns=['id', 'first_name', 'last_name'])
                # users['new'] = True
                sheet_reports =test.get_worksheet(3)
                geo_object = pd.DataFrame(sheet_reports.get_all_records(), columns=['geo_object_id', 'title', 'city'])
                unicreports = unicreports.merge(geo_object, left_on="geo_object_id", right_on="geo_object_id")

                merged_df = unicreports.merge(users, left_on="user_id", right_on="id")
                #   merged_df = unicreports.merge(users, left_on="user_id", right_on="id")
                merged_df['name'] = merged_df['first_name'].map(str) + ' ' + merged_df['last_name'].map(str) 
                merged_df= merged_df.drop(columns=['first_name', 'last_name', 'id'])
                merged_df = merged_df.sort_values(by='user_id')
                merged_df = merged_df[['user_id', 'name', 'geo_object_id', 'title', 'city', 'accepted', 'count']]
                
                a = merged_df
                # filtered_data = merged_df[merged_df["user_id"]==224]
                a = merged_df.loc[merged_df["user_id"].isin([224, 484695]), ['user_id', 'count']]
                print(a)
                print('Расчпечатано')
                # j.to_excel('данные.xlsx', index=False)
               
              
            # Загрузка данных с эксель файла 
                # df = pd.read_excel('данные.xlsx')
            # df = df.fillna('')

            # Получить названия всех колонок

            # test.update([df.columns.values.tolist()] + df.values.tolist())
            # df = pd.read_excel('A1.xlsx', header=2, usecols="A ,B" )
                # print(reports['user_id'])
                # print(users)
            except gspread.exceptions.SpreadsheetNotFound as err:
                print(err, 'Ошибка')
# # 
# Используется для первого задания для создания таблиц, импорт данных произведен внутри постресс
    def oneTable(self):
        mass = {
              'anketa':
            { 
                    'id': 'SERIAL PRIMARY KEY',
                    'subtype': ' VARCHAR(255) NULL',
                    'gs': ' VARCHAR(255) NULL',
                    'groups': ' VARCHAR(255) NULL',
                    'category': ' VARCHAR(255) NULL',
                    'subcategory': ' VARCHAR(255) NULL',
                    'epp': ' VARCHAR(255) NULL',
                    'ctm': 'VARCHAR(255) NULL',
                    'mgb': 'VARCHAR(255) NULL',
                    'metro': 'VARCHAR(255) NULL',
                    'schrih_code': 'VARCHAR(255) NULL',
                    'product_name': 'VARCHAR(255) NULL',
                    'need': 'VARCHAR(255) NULL',
                    'description': 'VARCHAR(255) NULL',
                    'regular_price': 'VARCHAR(255) NULL',
                    'promotional_price': 'VARCHAR(255) NULL',
                    'note': 'VARCHAR(255) NULL'
                }
            # 'questionnaire1':
            # { 
            #         'id': 'SERIAL PRIMARY KEY',
            #         'groups': 'VARCHAR(255) NOT NULL',
            #         'category': 'INTEGER NOT NULL',
            #         'subcategory': 'INTEGER NOT NULL',
            #         'epp': 'INTEGER NOT NULL',
            #         'ctm': 'INTEGER NULL',
            #         'cargo_code': 'INTEGER NOT NULL',
            #         'sub_cargo_code': 'INTEGER NOT NULL',
            #         'schrih_code': 'INTEGER NOT NULL',
            #         'product_name': 'VARCHAR(255) NOT NULL',
            #         'need': 'BOOLEAN NOT NULL',
            #         'monitoring_note': 'VARCHAR(255) NOT NULL',
            #         'regular_price': 'FLOAT NOT NULL',
            #         'promotional_price': 'FLOAT NOT NULL',
            #         'name_promotion': 'VARCHAR(255) NOT NULL'
            #     },
            #     'questionnaire2':
            #     {
            #         'id': 'SERIAL PRIMARY KEY',
            #         'subtype': ' VARCHAR(255) NOT NULL',
            #         'gs': ' VARCHAR(255) NOT NULL',
            #         'groups': ' VARCHAR(255) NOT NULL',
            #         'category': ' INTEGER NOT NULL',
            #         'subcategory': ' INTEGER NOT NULL',
            #         'epp': ' INTEGER NOT NULL',
            #         'ctm': 'INTEGER NULL',
            #         'cargo_code': 'INTEGER NOT NULL',
            #         'sub_cargo_code': 'INTEGER NOT NULL',
            #         'schrih_code': 'INTEGER NOT NULL',
            #         'product_name': 'VARCHAR(255) NOT NULL',
            #         'need': 'BOOLEAN NOT NULL',
            #         'monitoring_note': 'VARCHAR(255) NOT NULL',
            #         'regular_price': 'FLOAT NOT NULL',
            #         'promotional_price': 'FLOAT NOT NULL'
            #     }
                }

        for [key, val] in mass.items():
            self.connection.nameTable(key, val)

        pass

    





