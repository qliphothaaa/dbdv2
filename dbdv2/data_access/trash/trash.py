    def insertToDbdcompany(self,values):
        try:
            cur = self.db.cursor()
            query ='''INSERT INTO dbdcompany 
                        (DBD_ID, DBD_NAME_TH, DBD_REGISTRATION_DATE, DBD_REGISTRATION_MONEY,DBD_BUSINESS_TYPE_CODE,DBD_OBJECTIVE, DBD_STREET, DBD_SUBDISTRICT, DBD_DISTRICT, DBD_PROVINCE, DBD_ZIPCODE, DBD_ADDRESS)
                        VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    '''

            cur.execute(query, values)
            self.db.commit()
            print('insert into dbdcompany success',end=' ')
            print(values[1])#if insert success, It print value
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


    def insertTomdbd(self,values):
        try:
            cur = self.db.cursor()
            query ='''INSERT INTO mdbd
                        (id, regisid)
                        VALUES
                        (?, ?);
                    '''
            cur.execute(query, values)
            self.db.commit()
            print('insert into mdbd success',end='')
            print(values)


        except Exception as e:
            if e.errno == 1062:
                print('duplicate')
            else:
                print(e)
                print('fail to insert mdbd, rollback now')
            self.db.rollback()
        finally:
            cur.close()

    def getNewCompanyIdList(self):
        try:
            cur = self.db.cursor()
            query = 'select DBD_COMPANY_ID from dbd_new_query Where DBD_STATUS is NULL'
            cur.execute(query)
            ids = cur.fetchall()
        except Exception as e:
            print(e)
            print('fail to get information')
        finally:
            cur.close()
        return ids


    def getCompanyFailedIdList(self):
        try:
            cur = self.db.cursor()
            query = 'select DBD_COMPANY_ID from dbd_new_query Where DBD_STATUS = "Failed"'
            cur.execute(query)
            ids = cur.fetchall()
        except Exception as e:
            print(e)
            print('fail to get information')
        finally:
            cur.close()
        return ids

    def getAllCompanyIdList(self):
        try:
            cur = self.db.cursor()
            query = 'select DBD_COMPANY_ID from dbd_query'
            cur.execute(query)
            ids = cur.fetchall()
        except Exception as e:
            print(e)
            print('fail to get information')
        finally:
            cur.close()
        return ids
