from xls_reader import DbdExcelReader
import wget
import os
import sys
#need parameter url, (num)
num = 10000000
setting = ''
#print(len(sys.argv))
if len(sys.argv)>= 2:
    url = sys.argv[1]
    if len(sys.argv)>=3:
        num = sys.argv[2]
    if len(sys.argv)>=4:
        setting = sys.argv[3]
    #if len(month)==1 : month = '0'+month
    #datetime = year+month
    filename = url.split('/')[-1]

    filepath = './data_access/company_excel/' + filename
    print(filename)

    if not os.path.isfile(filepath):
        try:
            #url = 'https://www.dbd.go.th/download/document_file/Statisic/2562/XLS/99_%s.xls'% datetime
            #     'https://www.dbd.go.th/download/document_file/Statisic/2563/XLS/99_202001.xls'
            wget.download(url, './data_access/company_excel/')
            print('end')
        except Exception as e:
            print(e)
            print('cannot find the file')
            raise
    a = DbdExcelReader(filepath, num, setting)
    a.start()
else:
    raise Exception('not enough parameters')
    
