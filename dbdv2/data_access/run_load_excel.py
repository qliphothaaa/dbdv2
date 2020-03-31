from xls_reader import DbdExcelReader
from pdf_reader import DbdPDFReader
from dbd_connector import DbdConnector
import wget
import os
import sys
#need parameter url, (num)
setting = ''
#print(len(sys.argv))
if len(sys.argv)>= 2:
    url = sys.argv[1]
    if len(sys.argv)>=3:
        num = sys.argv[2]
    if len(sys.argv)>=4:
        setting = sys.argv[3]

    filename = url.split('/')[-1]
    print(filename)

    try:
        db = DbdConnector()

        sql = 'select count(*) from dbd_new_query where DBD_STATUS is null'
        if db.read(sql)[0] > 0:
            raise Exception(f'Error: There is unfinish work in new query!')

        sql = 'select count(*) from dbd_new_query where DBD_STATUS = "Failed"'
        if db.read(sql)[0] > 0:
            raise Exception(f'Error: There is unfinish work in new query!')
    finally:
        db.dbClose()
    


    if 'xls' in filename:
        filepath = './data_access/company_excel/' + filename
        if not os.path.isfile(filepath):
            try:
                wget.download(url, './data_access/company_excel/')
                print(f'download {filename} finished')
            except Exception as e:
                print(e)
                print('cannot find the excel file')
                raise
        a = DbdExcelReader(filepath, num, setting)
        a.start()

    elif 'pdf' in filename:
        filepath = './data_access/company_pdf/' + filename
        if not os.path.isfile(filepath):
            try:
                wget.download(url, './data_access/company_pdf/')
                print(f'download {filename} finished')
            except Exception as e:
                print(e)
                print('cannot find the pdf file')
                raise
        a = DbdPDFReader(filename, num)
        a.start()
    else:
        raise Exception(f'Error: this file ({filename}) is not support!')
else:
    raise Exception('Error: not enough parameters')
    
