import pandas as pd
import numpy as np
import datetime
try:
    from rex import address_clear, date_convert
except:
    from .rex import address_clear, date_convert
try:
    from dbd_connector import DbdConnector
except:
    from .dbd_connector import DbdConnector
import sys

#data = pd.read_excel('99_201901.xls', skiprows=2, nrows=10)


class DbdExcelReader(object):
    def __init__(self, xls_name, rows, column_setting=''):
        self.xls_name = xls_name#the xls_name of to find the excel file
        self.xls_path = './data_access/company_excel/'

        if rows == '':
            self.rows = None
        else:
            self.rows = int(rows)

        #self.column_setting = column_setting

        self.column_dict = {
            "ลำดับ": "ROW",
            "เลขทะเบียน":"ID", 
            "ชื่อนิติบุคคล":"NAME_TH", 
            "วันที่\nจดทะเบียน":"REGISTRATION_DATE", 
            "ทุนจดทะเบียน\n(บาท)":"REGISTRATION_MONEY", 
            "รหัส\nวัตถุประสงค์":"BUSINESS_TYPE_CODE", 
            "รายละเอียดวัตถุประสงค์":"OBJECTIVE",
            "ที่ตั้งสำนักงานใหญ่":"STREET",
            "ตำบล":"SUBDISTRICT",
            "อำเภอ":"DISTRICT",
            "จังหวัด":"PROVINCE",
            "รหัส\nไปรษณีย์":"ZIPCODE",
            "ทุนจดทะเบียน":"REGISTRATION_MONEY",
            }

    '''
    def enableColumnSetting(self):
        if self.column_setting:
            self.column_setting = self.column_setting.split(',')
            #print(self.column_setting)
            for i in self.column_setting:
                k, v = i.split(':')
                k = k.replace(" ", "\n")
                self.column_dict[k] = v
            #print(self.column_dict)
    '''


    def start(self):
        self.readExcel()
        self.checkData()
        self.hanldeData()
        self.insertData()

    def readExcel(self):
        self.data_dict = pd.read_excel(self.xls_path+self.xls_name, skiprows=2, converters={'เลขทะเบียน':str}, nrows=self.rows)# import excel file as pandas dataframe
        self.data_dict.rename(columns=self.column_dict,inplace=True)#change the column from thai to english
        

    def checkData(self):
        #check the column in excel is complete or not
        for i,v in self.column_dict.items():
            if not v in self.data_dict.columns:
                raise KeyError(f'can not find key {v} for {i}. Maybe the target changed the excel column, please check the excel file and add the changed column to variable. example:"ทุนจดทะเบียน:REGISTRATION_MONEY"')
        
        #replace wrong or empty information to NaN
        check_nan_df = pd.isnull(self.data_dict)
        position = np.where(check_nan_df)
        for i in range(len(position[0])):
            x = position[0][i]
            y = position[1][i]
            self.data_dict.iloc[x,y] = 'NaN'



        
    def hanldeData(self):
        self.data_dict['REGISTRATION_MONEY'] = self.data_dict['REGISTRATION_MONEY'].astype('str')
        self.data_dict['ZIPCODE'] = self.data_dict['ZIPCODE'].astype('str')
        self.data_dict['BUSINESS_TYPE_CODE'] = self.data_dict['BUSINESS_TYPE_CODE'].astype('str')
        #code above is to convert numpy.int64 to str. Because mysql cannot read int64

        self.data_dict['STREET'] = self.data_dict['STREET'].astype('str')
        self.data_dict['DISTRICT'] = self.data_dict['DISTRICT'].astype('str')
        self.data_dict['SUBDISTRICT'] = self.data_dict['SUBDISTRICT'].astype('str')
        #code above is to conver the street and district to string. Because some data in excel is wrong. I found there is a record that have datetime as subDistrict.

        

    def insertData(self):
        dbconnector = DbdConnector()
        print(f'insert {self.data_dict.shape[0]} datas to database')
        
        for i in range(self.data_dict.shape[0]):
            values = list(self.data_dict.loc[i])[1:]#the data_dict.loc[i] get a row of data as list, the first data in list is row number. 
            values[2] = date_convert(values[2])
            values[7], values[8], values[9] = address_clear(values[7], values[8], values[9])
            values.append(values[6] +' '+ values[7])
            value_id = (values[0], values[0][3])#values[0] is the company id. The 4th number of company id is typecode

            dbdcompany_sql = '''INSERT INTO dbdcompany 
                            (DBD_ID, DBD_NAME_TH, DBD_REGISTRATION_DATE, DBD_REGISTRATION_MONEY,DBD_BUSINESS_TYPE_CODE,DBD_OBJECTIVE, DBD_STREET, DBD_SUBDISTRICT, DBD_DISTRICT, DBD_PROVINCE, DBD_ZIPCODE, DBD_ADDRESS)
                            VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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
