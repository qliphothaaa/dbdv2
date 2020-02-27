from xls_reader import DbdExcelReader
import wget
import os
import sys
#need parameter year month, (num)
num = 10000000
if len(sys.argv)>2:
    year = sys.argv[1]
    month = sys.argv[2]
    if len(sys.argv)>3:
        num = sys.argv[3]
    if len(month)==1 : month = '0'+month
    datetime = year+month

    filename = './data_access/company_excel/' + '99_%s.xls' %datetime
    print(datetime)

    if not os.path.isfile(filename):
        try:
            url = 'https://www.dbd.go.th/download/document_file/Statisic/2562/XLS/99_%s.xls'% datetime
            wget.download(url, './data_access/company_excel/')
        except Exception as e:
            print(e)
            print('cannot find the file')
            raise

    a = DbdExcelReader(filename, num)
    a.start()
else:
    print('not enough parameter')
