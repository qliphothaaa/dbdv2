# -*- coding: utf-8 -*-
import mysql.connector
import time
from scrapy.exceptions import DropItem
from data_access.rex import *
from data_access.dbd_connector import DbdConnector


class MonthlyScrapingPipeline(object):
    def __init__(self):
        self.dbconnector = DbdConnector()

    def open_spider(self, spider):
        pass
        #self.cur = self.db.cursor()

    def close_spider(self, spider):
        pass
        #self.cur.close()

    def process_item(self, item, spider):
        scraping_status = item['scraping_status']
        company_id      = item['company_id']

        #if find data succeed
        if scraping_status:
            company_type = item['company_type']
            status       = item['status']
            objective    = item['objective']
            directors    = item['directors']
            company_name = item['company_name']
            raw_bussiness_type = item['bussiness_type']

            directors_text = ''
            for index, name in enumerate(directors):
                directors_text = directors_text + str(index)+'. '+name +'\n'
            directors_text = directors_text.rstrip()
            bussiness_type = business_type_separater(raw_bussiness_type)[1]

            company_name = re.split(':', company_name)[1].strip()


            #generate sql and valus
            sql_dbdcompany       = 'UPDATE dbdcompany SET DBD_TYPE = %s, DBD_STATUS= %s,DBD_OBJECTIVE = %s,DBD_DIRECTORS = %s, DBD_NAME_TH = %s, DBD_BUSINESS_TYPE = %s WHERE DBD_ID = %s;'
            values_dbdcompany    = (company_type, status, objective, directors_text, company_name, bussiness_type, company_id)

            sql_dbd_new_query    = 'update dbd_new_query set DBD_Status = "Success", DBD_LAST_RUN=%s where DBD_COMPANY_ID = %s'
            values_dbd_new_query = (time.strftime('%Y-%m-%d %H:%M:%S'), company_id)

            sql_dbd_query        = 'update dbd_query set DBD_Status = "Success", DBD_LAST_RUN=%s where DBD_COMPANY_ID = %s'
            values_dbd_query     = (time.strftime('%Y-%m-%d %H:%M:%S'), company_id)

            sqls   = (sql_dbdcompany, sql_dbd_new_query, sql_dbd_query)
            values = (values_dbdcompany, values_dbd_new_query, values_dbd_query)

            #update database
            self.dbconnector.updateCompanyTransaction(sqls, values, company_id)

            print('------------monthly update finished=====================')
            return item


        #if find data falied
        else:
            print('monthly scraping, failed to get the page')
            sql_dbd_new_query    = 'update dbd_new_query set DBD_Status = "Failed", DBD_LAST_RUN=%s where DBD_COMPANY_ID = %s'
            values_dbd_new_query = (time.strftime('%Y-%m-%d %H:%M:%S'), company_id)

            sql_dbd_query        = 'update dbd_query set DBD_Status = "Failed", DBD_LAST_RUN=%s where DBD_COMPANY_ID = %s'
            values_dbd_query     = (time.strftime('%Y-%m-%d %H:%M:%S'), company_id)

            sqls = (sql_dbd_new_query, sql_dbd_query)
            values = (values_dbd_new_query, values_dbd_query)

            self.dbconnector.updateCompanyTransaction(sqls, values, company_id)

            raise DropItem("cannot find the company %s" %item['company_id'])



class AnnuallyScrapingtPipeline(object):
    def __init__(self):
        self.dbconnector = DbdConnector()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def get_zipcode(self, address):
        zipcode = ''
        try:
            sql = f'SELECT ZIP from zipcodes where (SUBDISTRICT="{address[1]}" AND DISTRICT="{address[2]}" AND PROVINCE="{address[3]}");'
            zipcode = self.dbconnector.read(sql)[0]
            if zipcode == None: zipcode = ''
        except Exception as e:
            print(e)
        return zipcode
            
    def sql_generate(self, d):
        sql = ''
        for i in d.keys():
            sql = sql + i + '=' + f"'{d[i]}'"+', '
        sql = sql.rstrip(', ')

        return sql

    def get_old_data(self, company_id):
        sql = f'SELECT DBD_NAME_TH, DBD_STATUS, DBD_ADDRESS, DBD_OBJECTIVE, DBD_STREET, DBD_SUBDISTRICT, DBD_DISTRICT, DBD_PROVINCE, DBD_BUSINESS_TYPE_CODE, DBD_BUSINESS_TYPE, DBD_DIRECTORS, DBD_ZIPCODE from dbdcompany where DBD_ID = {company_id};'
        old_company_info = self.dbconnector.read(sql)

        old_company_dict = {'DBD_NAME_TH':old_company_info[0],
                            'DBD_STATUS':old_company_info[1],
                            'DBD_ADDRESS':old_company_info[2],
                            'DBD_OBJECTIVE':old_company_info[3],
                            'DBD_STREET':old_company_info[4],
                            'DBD_SUBDISTRICT':old_company_info[5],
                            'DBD_DISTRICT':old_company_info[6],
                            'DBD_PROVINCE':old_company_info[7],
                            'DBD_BUSINESS_TYPE_CODE':old_company_info[8],
                            'DBD_BUSINESS_TYPE':old_company_info[9],
                            'DBD_DIRECTORS':old_company_info[10],
                            'DBD_ZIPCODE':old_company_info[11]}
        return old_company_dict



    def process_item(self, item, spider):
        scraping_status = item['scraping_status']
        company_id      = item['company_id']
        if scraping_status:
            #new datas
            company_type       = item['company_type']
            status             = item['status']
            objective          = item['objective']
            directors          = item['directors']
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

            new_company_dict = {
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

            #old datas
            old_company_dict = self.get_old_data(company_id)

            #check datas
            update_dbdcompany_dict = {}

            update_query_dict = {}

            if new_company_dict['DBD_NAME_TH'] != old_company_dict['DBD_NAME_TH']:
                update_dbdcompany_dict['DBD_NAME_TH'] = new_company_dict['DBD_NAME_TH']
                update_query_dict['C_DBD_NAME_TH'] = new_company_dict['DBD_NAME_TH']

            if new_company_dict['DBD_STATUS'] != old_company_dict['DBD_STATUS']:
                update_dbdcompany_dict['DBD_STATUS'] = new_company_dict['DBD_STATUS']
                update_query_dict['C_DBD_STATUS'] = new_company_dict['DBD_STATUS']

            if new_company_dict['DBD_ADDRESS'] != old_company_dict['DBD_ADDRESS']:
                update_dbdcompany_dict['DBD_ADDRESS'] = new_company_dict['DBD_ADDRESS']
                update_query_dict['C_DBD_ADDRESS'] = new_company_dict['DBD_ADDRESS']

            if new_company_dict['DBD_OBJECTIVE'] != old_company_dict['DBD_OBJECTIVE']:
                update_dbdcompany_dict['DBD_OBJECTIVE'] = new_company_dict['DBD_OBJECTIVE']
                update_query_dict['C_DBD_OBJECTIVE'] = new_company_dict['DBD_OBJECTIVE']

            if new_company_dict['DBD_STREET'] != old_company_dict['DBD_STREET']:
                update_dbdcompany_dict['DBD_STREET'] = new_company_dict['DBD_STREET']
                update_query_dict['C_DBD_ADDRESS'] = new_company_dict['DBD_ADDRESS']

            if new_company_dict['DBD_SUBDISTRICT'] != old_company_dict['DBD_SUBDISTRICT']:
                update_dbdcompany_dict['DBD_SUBDISTRICT'] = new_company_dict['DBD_SUBDISTRICT']
                update_query_dict['C_DBD_ADDRESS'] = new_company_dict['DBD_ADDRESS']

            if new_company_dict['DBD_DISTRICT'] != old_company_dict['DBD_DISTRICT']:
                update_dbdcompany_dict['DBD_DISTRICT'] = new_company_dict['DBD_DISTRICT']
                update_query_dict['C_DBD_ADDRESS'] = new_company_dict['DBD_ADDRESS']

            if new_company_dict['DBD_PROVINCE'] != old_company_dict['DBD_PROVINCE']:
                update_dbdcompany_dict['DBD_PROVINCE'] = new_company_dict['DBD_PROVINCE']
                update_query_dict['C_DBD_ADDRESS'] = new_company_dict['DBD_ADDRESS']

            if new_company_dict['DBD_BUSINESS_TYPE_CODE'] != old_company_dict['DBD_BUSINESS_TYPE_CODE']:
                update_dbdcompany_dict['DBD_BUSINESS_TYPE_CODE'] = new_company_dict['DBD_BUSINESS_TYPE_CODE']
                update_query_dict['C_DBD_BUSINESS_TYPE'] = new_company_dict['DBD_BUSINESS_TYPE']

            if new_company_dict['DBD_BUSINESS_TYPE'] != old_company_dict['DBD_BUSINESS_TYPE']:
                update_dbdcompany_dict['DBD_BUSINESS_TYPE'] = new_company_dict['DBD_BUSINESS_TYPE']
                update_query_dict['C_DBD_BUSINESS_TYPE'] = new_company_dict['DBD_BUSINESS_TYPE']

            if new_company_dict['DBD_DIRECTORS'] != old_company_dict['DBD_DIRECTORS']:
                update_dbdcompany_dict['DBD_DIRECTORS'] = new_company_dict['DBD_DIRECTORS']

            if new_company_dict['DBD_ZIPCODE'] != old_company_dict['DBD_ZIPCODE']:
                update_dbdcompany_dict['DBD_ZIPCODE'] = new_company_dict['DBD_ZIPCODE']


            update_dbdcompany_string = self.sql_generate(update_dbdcompany_dict)
            update_query_string      = self.sql_generate(update_query_dict)
            

            #update dbdcompany
            if update_dbdcompany_string is not '':
                print(update_dbdcompany_string)
                sql_dbdcompany = f'UPDATE dbdcompany SET {update_dbdcompany_string} WHERE DBD_ID = {company_id};'
                if update_query_string is not '':
                    datetime = time.strftime('%Y-%m-%d %H:%M:%S')
                    sql_dbd_query = f'update dbd_query set DBD_STATUS ="Success", DBD_CHANGE=1, DBD_LAST_RUN="{datetime}", {update_query_string} where DBD_COMPANY_ID = {company_id}'
                else:
                    datetime = time.strftime('%Y-%m-%d %H:%M:%S')
                    sql_dbd_query = f'update dbd_query set DBD_STATUS ="Success", DBD_CHANGE=1, DBD_LAST_RUN="{datetime}" where DBD_COMPANY_ID = {company_id}'

                sqls = (sql_dbdcompany, sql_dbd_query)
                values = (None, None)

                self.dbconnector.updateCompanyTransaction(sqls, values, company_id)

                print(f'============update finieshed company {company_id}--------------')
            else:
                datetime = time.strftime('%Y-%m-%d %H:%M:%S')
                sql_dbd_query = f'update dbd_query set DBD_STATUS ="Success", DBD_CHANGE=0, DBD_LAST_RUN="{datetime}" where DBD_COMPANY_ID = {company_id}'
                sqls = (sql_dbd_query,)
                values = (None,)

                self.dbconnector.updateCompanyTransaction(sqls, values, company_id)
                print('------------nothing change in query=====================')

            return item

        else:
            sql_dbd_query        = 'update dbd_query set DBD_Status = "Failed", DBD_LAST_RUN=%s where DBD_COMPANY_ID = %s'
            values_dbd_query     = (time.strftime('%Y-%m-%d %H:%M:%S'), company_id)

            sqls = (sql_dbd_query,)
            values = (values_dbd_query,)

            self.dbconnector.updateCompanyTransaction(sqls, values, company_id)

            raise DropItem("cannot find the company %s" %item['company_id'])
            return item
