# для google_API
import httplib2
from googleapiclient import discovery  # вместо apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# для db_google_sheets
import psycopg2
from config import db_host, db_user, db_password, db_name
import requests
import xmltodict

# для логов
from datetime import datetime


# функция чтения гугл таблицы
def google_API():
    #подключение API
    
    CREDENTIALS_FILE = 'creds.json'  # файл с API
    spreadsheet_id = '1V-lsTLgKAZ7Kn90ARq3K84YsQxkD-h-mML2Xl0VATD8' # из url схемы таблицы гугл (тестовое)
    
    # документы с которыми будем работать
    creadentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    
    # создаем объект аунтификации
    httpAuth = creadentials.authorize(httplib2.Http())
    
    #создаем обертку API из которой мы будем получать данные из нашей схемы (v4 версия API sheets)
    service = discovery.build('sheets', 'v4', http=httpAuth)
       
    #Читаем данные 'A1:aA10' - диапозон, если весь то range='Лист1'
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Лист1',
        majorDimension='ROWS').execute()
    #pprint(values)
    return (values) 
    #exit()

# функция текущего курса долара
def cbr_usd_api():
    day = datetime.now().strftime("%d")
    mounth = datetime.now().strftime("%m")
    year = datetime.now().strftime("%Y")
    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{mounth}/{year}'
    xml = xmltodict.parse(requests.get(url).content)

    for value in xml['ValCurs']['Valute']:
        if value['@ID'] == 'R01235':
            #print(value['Name'])
            return(value['Value'])

#функция записи данных в БД PostgreSQL
def db_google_sheets():
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    try:
        #подключаемся к базе данных
        #создаем объект
        connection = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        connection.autocommit = True  # что бы не писать после каждого запроса коммит

        #для работы с БД нужно создать объект курсор (для выполнения различных команд SQl)
        with connection.cursor() as cursor:
            cursor.execute("""
            DROP TABLE IF EXISTS test;""")
            print(f'[{now}]: Drop old table "test" successfully')
    
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE test(
            id serial PRIMARY KEY,
            number integer,
            order_number integer,
            value_dolar int,
            value_rub int,
            delivery_time date);""")
            print(f'[{now}]: Create new table "test" successfully')

        values = google_API()
        print(f'[{now}]: Getting values Google Sheets successfully')

        usd = float(str(cbr_usd_api()).replace(',', '.'))
        print(f'[{now}]: Dollar rate {usd} rub')

        for i in range(1, len(values['values'])):
            number = values['values'][i][0]
            order_number = values['values'][i][1]
            value_dolar  = values['values'][i][2]
            value_rub = round(usd * int(value_dolar), 0)
            delivery_time  = values['values'][i][3]
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO test (number, order_number, value_dolar, value_rub, delivery_time) VALUES
                (%s, %s, %s, %s, %s);""",[int(number), int(order_number),
                                          int(value_dolar), value_rub, delivery_time])
        print(f'[{now}]: Insert values into table "test" successfully')

        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT test.number, order_number, delivery_time
            FROM test
            WHERE delivery_time < CURRENT_DATE
            ORDER BY delivery_time""")
            l1 = cursor.fetchall()
            return (l1)
            # print(l1)
            # for l in l1:
            #     print("Значения", l)
            #     print("*", l[1])
            #     print()


    except Exception as _ex:
        #обработка ошибок
        print(f'[{now}]: Error while working with PostgreSQL', _ex)
    finally:
        #закрываем подключение к БД
        if connection:
            connection.close()
            print(f'[{now}]: PostgreSQL connection closed')

