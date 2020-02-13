# -*- coding: utf-8 -*-
import mysql.connector
import time
from scrapy.exceptions import DropItem
from data_access.rex import *


class MonthlyScrapingPipeline(object):
    def __init__(self):
        self.db = mysql.connector.connect(
                host='dbd_db',
                user='root',
                passwd='1234',
                database='dbd'
                )
    def open_spider(self, spider):
        self.cur = self.db.cursor()

    def close_spider(self, spider):
        self.cur.close()

    def process_item(self, item, spider):
        scraping_status = item['scraping_status']
        if scraping_status:

            company_type = item['company_type']
            status       = item['status']
            objective    = item['objective']
            directors    = item['directors']
            company_id   = item['company_id']
            company_name = item['company_name']
            raw_bussiness_type = item['bussiness_type']

            directors_text = ''

            for index, name in enumerate(directors):
                directors_text = directors_text + str(index)+'. '+name +'\n'
            directors_text = directors_text.rstrip()
            bussiness_type = business_type_separater(raw_bussiness_type)[1]

            company_name = re.split(':', company_name)[1].strip()

            try:
                sql = 'UPDATE dbdcompany SET DBD_TYPE = %s, DBD_STATUS= %s,DBD_OBJECTIVE = %s,DBD_DIRECTORS = %s, DBD_NAME_TH = %s, DBD_BUSINESS_TYPE = %s WHERE DBD_ID = %s;'
                values = (company_type, status, objective, directors_text, company_name, bussiness_type, company_id)
                self.cur.execute(sql, values)
                self.db.commit()
                print(self.cur.rowcount, "record(s) affected")
            except Exception as e:
                print(e)
                self.db.rollback()
                return item
            print('------------update dbd_company finished=====================')

            try:
                sql = 'update dbd_new_query set DBD_Status = "Success", DBD_LAST_RUN=%s where DBD_COMPANY_ID = %s'
                values = (time.strftime('%Y-%m-%d %H:%M:%S'), company_id)
                self.cur.execute(sql, values)
                self.db.commit()
                print(self.cur.rowcount, "record(s) affected")
            except Exception as e:
                print(e)
                self.db.rollback()
            print('------------update dbd_new_query finished=====================')

            try:
                sql = 'update dbd_query set DBD_Status = "Success", DBD_LAST_RUN=%s where DBD_COMPANY_ID = %s'
                values = (time.strftime('%Y-%m-%d %H:%M:%S'), company_id)
                self.cur.execute(sql, values)
                self.db.commit()
                print(self.cur.rowcount, "record(s) affected")
            except Exception as e:
                print(e)
                self.db.rollback()
            print('------------update dbd_query finished=====================')


        else:
            try:
                sql = 'update dbd_new_query set DBD_Status = "Failed", DBD_LAST_RUN=%s where DBD_COMPANY_ID = %s'
                values = (time.strftime('%Y-%m-%d %H:%M:%S'), company_id)
                self.cur.execute(sql, values)
                self.db.commit()
                print(self.cur.rowcount, "record(s) affected")
            except Exception as e:
                print(e)
                self.db.rollback()
            print('------------update dbd_new_query finished=====================')

            try:
                sql = 'update dbd_query set DBD_Status = "Failed", DBD_LAST_RUN=%s, DBD_IGNORE=1 where DBD_COMPANY_ID = %s'
                values = (time.strftime('%Y-%m-%d %H:%M:%S'), company_id)
                self.cur.execute(sql, values)
                self.db.commit()
                print(self.cur.rowcount, "record(s) affected")
            except Exception as e:
                print(e)
                self.db.rollback()
            print('------------update dbd_query finished=====================')

            raise DropItem("cannot find the company %s" %item['company_id'])

        return item



class AnnuallyScrapingtPipeline(object):
    def __init__(self):
        self.db = mysql.connector.connect(
                host='dbd_db',
                user='root',
                passwd='1234',
                database='dbd'
                )
    def open_spider(self, spider):
        self.cur = self.db.cursor(buffered=True)

    def close_spider(self, spider):
        self.cur.close()

    def get_zipcode(self, address):
        zipcode = ''
        try:
            sql = f'SELECT ZIP from zipcodes where (SUBDISTRICT="{address[1]}" AND DISTRICT="{address[2]}" AND PROVINCE="{address[3]}");'
            self.cur.execute(sql)
            zipcode = self.cur.fetchone()[0]
            if zipcode == None: zipcode = ''
        except Exception as e:
            print(e)
        return zipcode
            
    def sql_generate(self, d):
        update_string = ''
        for i in d.keys():
            update_string = update_string + i + '=' + f"'{d[i]}'"+', '
        update_string = update_string.rstrip(', ')

        return update_string



    def process_item(self, item, spider):
        scraping_status = item['scraping_status']
        if scraping_status:

            company_type       = item['company_type']
            status             = item['status']
            objective          = item['objective']
            directors          = item['directors']
            company_id         = item['company_id']
            company_name       = item['company_name']
            raw_bussiness_type = item['bussiness_type']
            raw_address        = item['address']

            company_name   = re.split(':', company_name)[1].strip()
            directors_text = ''
            for index, name in enumerate(directors):
                directors_text = directors_text + str(index)+'. '+name +'\n'
            directors_text = directors_text.rstrip()
            bussiness_type = business_type_separater(raw_bussiness_type)
            address        = address_separater(raw_address)
            zipcode = self.get_zipcode(address)

            sql = f'SELECT DBD_NAME_TH, DBD_STATUS, DBD_ADDRESS, DBD_OBJECTIVE, DBD_STREET, DBD_SUBDISTRICT, DBD_DISTRICT, DBD_PROVINCE, DBD_BUSINESS_TYPE_CODE, DBD_BUSINESS_TYPE, DBD_DIRECTORS, DBD_ZIPCODE from dbdcompany where DBD_ID = {company_id};'
            self.cur.execute(sql)
            old_company_info = self.cur.fetchone()

            update_dbdcompany_dict = {
                    'DBD_NAME_TH':company_name, 
                    'DBD_STATUS':status, 
                    'DBD_ADDRESS':address[0]+ ' ' +address[1], 
                    'DBD_OBJECTIVE':objective, 
                    'DBD_STREET':address[0], 
                    'DBD_SUBDISTRICT':address[1], 
                    'DBD_DISTRICT':address[2], 
                    'DBD_PROVINCE':address[3], 
                    'DBD_BUSINESS_TYPE_CODE':bussiness_type[0], 
                    'DBD_BUSINESS_TYPE':bussiness_type[1], 
                    'DBD_DIRECTORS':directors_text,
                    'DBD_ZIPCODE':zipcode
                    }

            update_query_dict = {
                    'C_DBD_NAME_TH':company_name, 
                    'C_DBD_STATUS':status, 
                    'C_DBD_ADDRESS':address[0]+address[1], 
                    'C_DBD_OBJECTIVE':objective, 
                    'C_DBD_BUSINESS_TYPE':bussiness_type[1], 
                    }

            if update_dbdcompany_dict['DBD_NAME_TH'] == old_company_info[0]:
                update_dbdcompany_dict.pop('DBD_NAME_TH')
                update_query_dict.pop('C_DBD_NAME_TH')
            if update_dbdcompany_dict['DBD_STATUS'] == old_company_info[1]:
                update_dbdcompany_dict.pop('DBD_STATUS')
                update_query_dict.pop('C_DBD_STATUS')
            if update_dbdcompany_dict['DBD_ADDRESS'] == old_company_info[2]:
                update_dbdcompany_dict.pop('DBD_ADDRESS')
                update_query_dict.pop('C_DBD_ADDRESS')
            if update_dbdcompany_dict['DBD_OBJECTIVE'] == old_company_info[3]:
                update_dbdcompany_dict.pop('DBD_OBJECTIVE')
                update_query_dict.pop('C_DBD_OBJECTIVE')
            if update_dbdcompany_dict['DBD_STREET'] == old_company_info[4]:
                update_dbdcompany_dict.pop('DBD_STREET')
            if update_dbdcompany_dict['DBD_SUBDISTRICT'] == old_company_info[5]:
                update_dbdcompany_dict.pop('DBD_SUBDISTRICT')
            if update_dbdcompany_dict['DBD_DISTRICT'] == old_company_info[6]:
                update_dbdcompany_dict.pop('DBD_DISTRICT')
            if update_dbdcompany_dict['DBD_PROVINCE'] == old_company_info[7]:
                update_dbdcompany_dict.pop('DBD_PROVINCE')
            if update_dbdcompany_dict['DBD_BUSINESS_TYPE_CODE'] == old_company_info[8]:
                update_dbdcompany_dict.pop('DBD_BUSINESS_TYPE_CODE')
            if update_dbdcompany_dict['DBD_BUSINESS_TYPE'] == old_company_info[9]:
                update_dbdcompany_dict.pop('DBD_BUSINESS_TYPE')
                update_query_dict.pop('C_DBD_BUSINESS_TYPE')
            if update_dbdcompany_dict['DBD_DIRECTORS'] == old_company_info[10]:
                update_dbdcompany_dict.pop('DBD_DIRECTORS')
            if update_dbdcompany_dict['DBD_ZIPCODE'] == old_company_info[11]:
                update_dbdcompany_dict.pop('DBD_ZIPCODE')

            update_dbdcompany_string = self.sql_generate(update_dbdcompany_dict)
            update_query_string = self.sql_generate(update_query_dict)
            

            if update_dbdcompany_string is not '':
                try:
                    sql = f'UPDATE dbdcompany SET {update_dbdcompany_string} WHERE DBD_ID = {company_id};'
                    print(sql)
                    self.cur.execute(sql)
                    self.db.commit()
                    print(self.cur.rowcount, "record(s) affected")
                except Exception as e:
                    print(e)
                    self.db.rollback()
                    return item
                print('------------update dbd_company finished=====================')
            else:
                print('-------------nothing change-------------')


            #update dbd_query
            if update_query_string is not '':
                try:
                    datetime = time.strftime('%Y-%m-%d %H:%M:%S')
                    sql = f'update dbd_query set DBD_STATUS ="Success", DBD_CHANGE=1, DBD_LAST_RUN="{datetime}", {update_query_string} where DBD_COMPANY_ID = {company_id}'
                    print(sql)
                    self.cur.execute(sql)
                    self.db.commit()
                    print(self.cur.rowcount, "record(s) affected")
                except Exception as e:
                    print(e)
                    self.db.rollback()
                print('------------update dbd_query finished=====================')
            else:
                try:
                    datetime = time.strftime('%Y-%m-%d %H:%M:%S')
                    sql = f'update dbd_query set DBD_STATUS ="Success", DBD_CHANGE=0, DBD_LAST_RUN="{datetime}" where DBD_COMPANY_ID = {company_id}'
                    self.cur.execute(sql)
                    self.db.commit()
                    print(self.cur.rowcount, "record(s) affected")
                except Exception as e:
                    print(e)
                    self.db.rollback()
                print('------------update finished, nothing change=====================')



        else:

            try:
                sql = 'update dbd_query set DBD_Status = "Failed", DBD_LAST_RUN=%s, DBD_IGNORE=1 where DBD_COMPANY_ID = %s'
                values = (time.strftime('%Y-%m-%d %H:%M:%S'), company_id)
                self.cur.execute(sql, values)
                self.db.commit()
                print(self.cur.rowcount, "record(s) affected")
            except Exception as e:
                print(e)
                self.db.rollback()
            print('------------update dbd_query finished=====================')

            raise DropItem("cannot find the company %s" %item['company_id'])

        return item
