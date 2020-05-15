import pandas as pd
import numpy as np
import pdfplumber
import datetime
import time
try:
    from dbd_connector import DbdConnector
except:
    from .dbd_connector import DbdConnector

try:
    from rex import date_convert
except:
    from .rex import date_convert

import sys



class DbdPDFReader(object):
    def __init__(self, pdf_name, rows):
        self.pdf_name = pdf_name#the name of the pdf file
        if rows == '':
            self.rows = None
        else:
            self.rows = int(rows)
        extension = pdf_name.split('.')[-1]
        self.filename = pdf_name.rstrip('.' + extension)
        self.pdf_path = 'data_access/company_pdf/'
        self.csv_path = 'data_access/company_csv/'

    def start(self):
        print(f'start to read {self.pdf_name}')
        self.readPDF()
        self.readCSV()
        self.checkData()
        self.hanldeData()

        #oldtime=datetime.datetime.now()
        self.insertData()
        #newtime=datetime.datetime.now()
        #print(newtime-oldtime)

    def readPDF(self):
        pdf = pdfplumber.open(self.pdf_path + self.pdf_name)
        total_pd = pd.DataFrame()

        finished_rows = 0

        for page in range(len(pdf.pages)):
            if isinstance(self.rows, int) and finished_rows > self.rows:
                break
            print(f'page No.{page}')
            temp_table = pdf.pages[page].extract_table()
            finished_rows += len(temp_table)-1
            temp_df = pd.DataFrame(temp_table[1:])
            temp_df.replace(to_replace = r'\n', value = '', regex = True, inplace = True)
            total_pd = pd.concat([total_pd, temp_df], ignore_index = True)
        total_pd = total_pd.drop([0,2,5,6,7,8,9,10],axis=1)
        self.data_dict = total_pd
        self.data_dict.to_csv(self.csv_path + self.filename + '.csv', index = False, header = False)
        print(f'successfully transfer pdf to csv file in {self.csv_path+self.filename + ".csv"}')


    def readCSV(self):
        self.data_dict = pd.read_csv(self.csv_path+self.filename+'.csv', nrows=self.rows, header=None, dtype=str)#, index_col=0)
        #print(self.data_dict.shape)
        print(self.data_dict)


        

    def checkData(self):
        check_nan_df = pd.isnull(self.data_dict)
        position = np.where(check_nan_df)
        for i in range(len(position[0])):
            x = position[0][i]
            y = position[1][i]
            self.data_dict.iloc[x,y] = 'NaN'



        
    def hanldeData(self):
        #self.data_dict[1] = self.data_dict[1].astype('str')
        #self.data_dict = self.data_dict.drop([0,2,3,4,5,6,7,8,9,10,11],axis=1)
        print(self.data_dict)


    def insertData(self):
        dbconnector = DbdConnector()
        
        for i in range(self.data_dict.shape[0]):
            values = list(self.data_dict.loc[i])#the data_dict.loc[i] get a row of data as list, the first data in list is row number. 
            values[1] = date_convert(values[1])
            values[2] = values[2].replace(',','').replace(' ','')
            value_id = (values[0], values[0][3])#values[0] is the company id. The 4th number of company id is typecode

            dbdcompany_sql = '''INSERT INTO dbdcompany 
                            (DBD_ID, DBD_REGISTRATION_DATE, DBD_REGISTRATION_MONEY, DBD_ZIPCODE)
                            VALUES
                            (%s, %s, %s, %s);
                            '''
            dbd_new_query_sql = '''INSERT INTO dbd_new_query
                            (DBD_COMPANY_ID, DBD_TYPECODE)
                            VALUES
                            (%s, %s);
                            '''
            dbd_query_sql = '''INSERT INTO dbd_query
                            (DBD_COMPANY_ID, DBD_TYPECODE)
                            VALUES
                            (%s, %s);
                            '''
            sqls = (dbdcompany_sql, dbd_new_query_sql, dbd_query_sql)
            values_tuple = (values, value_id, value_id)
            dbconnector.insertTransaction(sqls, values_tuple)
            
        dbconnector.dbClose()



if __name__ == "__main__":
    a = DbdPDFReader('99.pdf', 100000000)
    a.start()
