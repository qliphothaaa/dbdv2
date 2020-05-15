from dbd_connector import DbdConnector
from serializer import MdbdSerializer 
from csv_reader import DbdCSVReader
from xls_reader import DbdExcelReader
from pdf_reader import DbdPDFReader
import os
import sys

EXPORT_PATH = './data_access/export/'
EXCEL_PATH = './data_access/company_excel/'
PDF_PATH = './data_access/company_pdf/'
CSV_PATH = './data_access/customer_csv/'

def loadfile(filename, num):
    try:
        db = DbdConnector()

        sql = 'select count(*) from dbd_new_query where DBD_STATUS is null'
        if db.read(sql)[0] > 0:
            raise Exception(f'Error: There is unfinish work in new query!')

        sql = 'select count(*) from dbd_new_query where DBD_STATUS = "Failed"'
        if db.read(sql)[0] > 0:
            raise Exception(f'Error: There is failed work in new query!')
    finally:
        db.dbClose()

    a = DbdConnector()
    a.clearNewQuery()
    a.dbClose()
    
    if 'xls' in filename:
        filepath = EXCEL_PATH + filename
        if os.path.isfile(filepath):
            a = DbdExcelReader(filename, num)
            a.start()
        else:
            raise Exception('cannot find the xls file')
    elif 'pdf' in filename:
        filepath = PDF_PATH + filename
        if os.path.isfile(filepath):
            a = DbdPDFReader(filename, num)
            a.start()
        else:
            raise Exception('cannot find the pdf file')
    else:
        raise Exception(f'Error: this file ({filename}) is not support!')

def loadcsv(filename, num):
    a = DbdConnector()
    a.clearmdbd()
    a.dbClose()

    path = CSV_PATH +file_name
    if os.path.isfile(path):
        a = DbdCSVReader(path , num)
        a.start()
    else:
        raise Exception('cannot find the csv file')


if len(sys.argv)>1:
    function = sys.argv[1]

    if function == 'lf':
        print('load file')
        filename = sys.argv[2]
        if len(sys.argv)>=4:
            num = sys.argv[3]
        else:
            num = ''
        loadfile(filename, num)

    elif function == 'lc':
        print('loadcsv')
        file_name = sys.argv[2]
        if len(sys.argv)>3:
            num = sys.argv[3]
        else:
            num = 10000000
        loadcsv(file_name, num)

    elif function == 'ed':
        print('export data')
        if len(sys.argv)>2:
            limit = sys.argv[2]
        else:
            limit = 2000000


        if os.path.isdir(EXPORT_PATH):
            serializer = MdbdSerializer(EXPORT_PATH, limit)
            serializer.start_export_newcompany()
        else:
            raise Exception('no path to export file')

    elif function == 'eda':
        print('export data all')
        if len(sys.argv)>2:
            limit = sys.argv[2]
        else:
            limit = 2000000


        if os.path.isdir(EXPORT_PATH):
            serializer = MdbdSerializer(EXPORT_PATH, limit)
            serializer.start_export_allcompany()
        else:
            raise Exception('no path to export file')

    elif function == 'help':
        print('lf filename [number]               "load file to database (pdf or xls)"')
        print('')
        print('lc filename [number]               "load file to database (csv)"')
        print('')
        print('ed [limite]                        "export one month data"')
        print('')
        print('eda [limite]                       "export all data"')
        print('')
else:
    raise Exception('Error: not enough parameters')




