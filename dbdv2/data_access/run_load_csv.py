from csv_reader import DbdCSVReader
import os
import sys

#a = DbdCSVReader('./data_access/customer_csv/28012020.csv', 5039)
#a.start()

#need parameter file_name, (num)
num = 10000000
if len(sys.argv)>1:
    file_name = sys.argv[1]
    if len(sys.argv)>2:
        num = sys.argv[2]
    path = './data_access/customer_csv/'+file_name
    if os.path.isfile(path):
        a = DbdCSVReader(path , num)
        a.start()
    else:
        print('cannot find the csv file')
else:
    print('not enough parameter')
