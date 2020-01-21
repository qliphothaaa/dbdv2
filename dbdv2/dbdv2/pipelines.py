# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
import time
from scrapy.exceptions import DropItem


class Dbdv2Pipeline(object):
    def __init__(self):
        self.db = mysql.connector.connect(
                host='dbd_database_1',
                user='root',
                passwd='1234',
                database='dbd'
                )
    def open_spider(self, spider):
        self.cur = self.db.cursor()

    def close_spider(self, spider):
        self.cur.close()

    def process_item(self, item, spider):
        company_type = item['company_type']
        status       = item['status']
        objective    = item['objective']
        directors    = item['directors']
        company_id   = item['company_id']

        if status != None:

            directors_text = ''
            for index, name in enumerate(directors):
                directors_text = directors_text + str(index)+'. '+name +'\n'
            directors_text = directors_text.rstrip()


            try:
                sql = 'UPDATE dbdcompany SET DBD_TYPE = %s, DBD_STATUS= %s,DBD_OBJECTIVE = %s,DBD_DIRECTORS = %s WHERE DBD_ID = %s;'
                values = (company_type, status, objective, directors_text, company_id)
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
