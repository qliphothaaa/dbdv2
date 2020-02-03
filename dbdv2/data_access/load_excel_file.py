from xls_reader import DbdExcelReader
import wget, os, sys
num = 10
if len(sys.argv)>2:
    year = sys.argv[1]
    month = sys.argv[2]
    if len(sys.argv)>3:
        num = sys.argv[3]
    if len(month)==1 : month = '0'+month
    datetime = year+month

    url = 'https://www.dbd.go.th/download/document_file/Statisic/2562/XLS/99_%s.xls'% datetime
    filename = './data_access/company_excel/' + '99_%s.xls' %datetime

    if not os.path.isfile(filename):
        wget.download(url, './data_access/company_excel/')

    a = DbdExcelReader(filename, num)
    a.start()
