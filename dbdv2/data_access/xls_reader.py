import pandas as pd
import numpy as np
try:
    from dbd_connector import DbdConnector
except:
    from .dbd_connector import DbdConnector
import sys

#data = pd.read_excel('99_201901.xls', skiprows=2, nrows=10)


class DbdExcelReader(object):
    def __init__(self, path, rows=1):
        self.path = path#the path of to find the excel file
        self.rows = int(rows)

    def start(self):
        self.readExcel()
        self.checkData()
        self.hanldeData()
        self.insertData()

    def readExcel(self):
        #self.data_dict = pd.read_excel(self.path, skiprows=2)
        self.data_dict = pd.read_excel(self.path, skiprows=2, converters={'เลขทะเบียน':str}, nrows=self.rows)# import excel file as pandas dataframe
        self.data_dict.rename(columns={
            "ลำดับ": "ROW",
            "เลขทะเบียน":"ID", 
            "ชื่อนิติบุคคล":"NAME_TH", 
            "วันที่\nจดทะเบียน":"REGISTRATION_DATE", 
            "ทุนจดทะเบียน\n(บาท)":"REGISTRATION_MONEY", 
            "รหัส\nวัตถุประสงค์":"BUSINESS_TYPE_CODE", 
            "รายละเอียดวัตถุประสงค์":"BUSINESS_TYPE",
            "ที่ตั้งสำนักงานใหญ่":"STREET",
            "ตำบล":"SUBDISTRICT",
            "อำเภอ":"DISTRICT",
            "จังหวัด":"PROVINCE",
            "รหัส\nไปรษณีย์":"ZIPCODE",
            },inplace=True)#change the column from thai to english
        

    def checkData(self):
        check_nan_df = pd.isnull(self.data_dict)
        position = np.where(check_nan_df)
        for i in range(len(position[0])):
            x = position[0][i]
            y = position[1][i]
            self.data_dict.iloc[x,y] = 'NaN'



        
    def hanldeData(self):
        #self.data_dict['ID'] = self.data_dict['ID'].astype('str')
        self.data_dict['REGISTRATION_MONEY'] = self.data_dict['REGISTRATION_MONEY'].astype('str')
        self.data_dict['ZIPCODE'] = self.data_dict['ZIPCODE'].astype('str')
        self.data_dict['BUSINESS_TYPE_CODE'] = self.data_dict['BUSINESS_TYPE_CODE'].astype('str')
        #code above is to convert numpy.int64 to str. Because mysql cannot read int64

        self.data_dict['STREET'] = self.data_dict['STREET'].astype('str')
        self.data_dict['DISTRICT'] = self.data_dict['DISTRICT'].astype('str')
        self.data_dict['SUBDISTRICT'] = self.data_dict['SUBDISTRICT'].astype('str')
        #code above is to conver the street and district to string. Because some data in excel is wrong. I found there is a record that have datetime as subDistrict.
        #it lead to error. maybe I will check the data later.

        self.data_dict['ADDRESS'] = self.data_dict['STREET']+' '+self.data_dict['SUBDISTRICT']
        #combine street and subdistrict to create address.
        

    def insertData(self):
        dbconnector = DbdConnector()
        
        for i in range(self.data_dict.shape[0]):
            values = list(self.data_dict.loc[i])[1:]#the data_dict.loc[i] get a row of data as list, the first data in list is row number. 
            value_id = (values[0], values[0][3])#values[0] is the company id. The 4th number of company id is typecode

            dbconnector.insertToDbdcompany(values)
            dbconnector.insertToDbdNewQuery(value_id)
            dbconnector.insertToDbdQuery(value_id)
            
        dbconnector.dbClose()


    #below here is some trash

    '''
    def check(self, df):
        if df.empty:
            print('warning: %s is empty' % (df.columns[0]) )
        print('%s: %d records' % (df.columns[0], df.shape[0]))
        #print(df)


    def getData(self,num):
        def getDataFromDF(df):
            return str(df[df.columns[0]][num])
        return getDataFromDF
    '''



        
