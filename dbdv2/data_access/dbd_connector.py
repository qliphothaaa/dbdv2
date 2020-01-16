import mysql.connector
import datetime

class DbdConnector(object):
    def __init__(self):
        self.db = mysql.connector.connect(
                host='localhost', 
                user='root', 
                passwd='qliphoth',
                database='dbd'
                )
        

    def insertToDbdcompany(self,values):
        try:
            cur = self.db.cursor()
            '''
            for value in values:
                print(type(value))
            '''
            query ='''INSERT INTO dbdcompany 
                        (DBD_ID, DBD_NAME_TH, DBD_REGISTRATION_DATE, DBD_REGISTRATION_MONEY,DBD_BUSINESS_TYPE_CODE,DBD_BUSINESS_TYPE, DBD_STREET, DBD_SUBDISTRICT, DBD_DISTRICT, DBD_PROVINCE, DBD_ZIPCODE, DBD_ADDRESS)
                        VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    '''

            cur.execute(query, values)
            self.db.commit()
            print('insert into dbdcompany success',end=' ')
            print(values[0])#if insert success, It print value
        except Exception as e:
            
            if e.errno == 1062:#the code when the data already in database
                print('duplicate')
            else:
                print(e)
                print('fail to insert into dbdcompany, rollback now')
            self.db.rollback()
        finally:
            cur.close()


    def insertToDbdQuery(self,values):
        try:
            cur = self.db.cursor()
            query ='''INSERT INTO dbd_query
                        (DBD_COMPANY_ID, DBD_TYPECODE)
                        VALUES
                        (%s, %s);
                    '''

            cur.execute(query, values)
            self.db.commit()
            print('insert into dbd_query success',end='')
            print(values)
        except Exception as e:
            if e.errno == 1062:
                print('duplicate')
            else:
                print(e)
                print('fail to insert dbd_query, rollback now')
            self.db.rollback()
        finally:
            cur.close()


    def insertToDbdNewQuery(self,values):
        try:
            cur = self.db.cursor()
            query ='''INSERT INTO dbd_new_query
                        (DBD_COMPANY_ID, DBD_TYPECODE)
                        VALUES
                        (%s, %s);
                    '''

            cur.execute(query, values)
            self.db.commit()
            print('insert into dbd_new_query success',end='')
            print(values)
        except Exception as e:
            if e.errno == 1062:
                print('duplicate')
            else:
                print(e)
                print('fail to insert dbd_new_query, rollback now')
            self.db.rollback()
        finally:
            cur.close()


    def dbClose(self):
        self.db.close()
        print("database close")

    def getCompanyIdList(self):
        try:
            cur = self.db.cursor()
            query = ' select DBD_COMPANY_ID from dbd_new_query'
            cur.execute(query)
            ids = cur.fetchall()
        except Exception as e:
            print(e)
            print('fail to get information')
        finally:
            cur.close()
        return ids


if __name__ == '__main__':
    db = DbdConnector()
    '''
    data = ('123', 'my company', datetime.datetime.now(), 20000, '34522', 'type', 'street', 'subd', 'dist', 'prov', '12345', 'address')
    db.insertToDbdcompany(data)
    '''
    db.getCompanyIdList()

        
