import pandas as pd
import mysql.connector
import numpy as np
import datetime

try:
    from dbd_connector import DbdConnector
except:
    from .dbd_connector import DbdConnector

import sys



class DbdCSVReader(object):
    def __init__(self, path, rows):
        self.path = path#the path of to find the excel file
        self.rows = int(rows)

    def start(self):
        oldtime=datetime.datetime.now()
        self.read()
        newtime=datetime.datetime.now()
        #print(newtime-oldtime)

        self.checkData()
        self.hanldeData()

        oldtime=datetime.datetime.now()
        self.insertData()
        newtime=datetime.datetime.now()
        print(newtime-oldtime)

    def read(self):
        self.data_dict = pd.read_csv(self.path, nrows=self.rows)
        print(self.data_dict.shape)
        #for i in range(0, self.data_dict.shape[0]):
            #print(self.data_dict.iloc[i])
        #print(self.data_dict.shape)
        #print(self.data_dict)


    def checkData(self):
        check_nan_df = pd.isnull(self.data_dict)
        position = np.where(check_nan_df)
        for i in range(len(position[0])):
            x = position[0][i]
            y = position[1][i]
            self.data_dict.iloc[x,y] = 'NaN'
            print('NaN detected')

        
    def hanldeData(self):
        self.data_dict['dbdcompaniesid'] = self.data_dict['dbdcompaniesid'].astype('str')
        self.data_dict['cf_755'] = '0'+ self.data_dict['cf_755'].astype('str')
        #self.data_dict.sort_values(by=['dbdcompaniesid'], ascending=True, inplace=True)

        

    def insertData(self):
        dbconnector = DbdConnector()
        
        #print(self.data_dict)
        #for i in reversed(range(self.data_dict.shape[0])):
        count = 0
        a = 0
        vl = []
        for i in range(self.data_dict.shape[0]):
            values = list(self.data_dict.loc[i])#the data_dict.loc[i] get a row of data as list, the first data in list is row number. 
            vl.append(values[0])
            vl.append(values[1])
            #print(values)
            count += 1
            a += 1
            if a == 5000:
                sql = "INSERT INTO mdbd(id, regisid)VALUES" + '(%s, %s),'*a
                sql = sql.rstrip(',')
                dbconnector.insert(sql, vl)
                a = 0
                vl = []

        sql = "INSERT INTO mdbd(id, regisid)VALUES" + '(%s, %s),'*a
        sql = sql.rstrip(',')
        dbconnector.insert(sql, vl)

        #dbconnector.insert("INSERT INTO mdbd(id, regisid)VALUES(%s, %s);", values)
        print(f'totally {count} datas')
            
        dbconnector.dbClose()


if __name__ == '__main__':
    a = DbdCSVReader('./data_access/customer_csv/28012020.csv', 5039)
    a.start()

