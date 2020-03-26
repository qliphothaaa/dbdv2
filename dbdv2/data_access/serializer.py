import time
import sys
try:
    from dbd_connector import DbdConnector
except:
    from .dbd_connector import DbdConnector

class MdbdSerializer(object):
    def __init__(self, path, limit):
        self.path = path
        self.db_connector = DbdConnector()
        try:
            self.recent_id = self.db_connector.find_biggest_id(limit)[0]
        except TypeError:
            print('no enough id for insert! please check the mdbd table!')
            print(f'The limitation is < {limit}')
            sys.exit()
        #self.dbd_company_template = ('DBD_ID', 'DBD_TYPE', 'DBD_REGISTRATION_DATE', 'DBD_STATUS', 'DBD_REGISTRATION_MONEY', 'DBD_STREET', 'DBD_SUBDISTRICT', 'DBD_DISTRICT', 'DBD_PROVINCE', 'DBD_ZIPCODE', 'DBD_BUSINESS_TYPE_CODE', 'DBD_BUSINESS_TYPE', 'DBD_OBJECTIVE', 'DBD_NAME_TH')
        self.company_template = ("cf_755", "cf_757","cf_763","cf_759","cf_761","cf_809","cf_811","cf_813","cf_815","cf_817","cf_799","cf_801","cf_1995","dbdcompanies")


    def start_export_newcompany(self):
        include_id_generator = self.get_include_company_data()
        exclude_id_generator = self.get_exclude_company_data()
        self.write_update_file(include_id_generator)
        self.write_insert_file(exclude_id_generator)
        self.db_connector.dbClose()

    def start_export_allcompany(self):
        include_id_generator = self.get_include_company_data_all()
        exclude_id_generator = self.get_exclude_company_data_all()
        self.write_update_file(include_id_generator, 'DBD')
        self.write_insert_file(exclude_id_generator, 'DBD')
        self.db_connector.dbClose()


    def get_include_company_data(self):
        include_company_ids =  self.db_connector.read_include_new_company()
        for company_id in include_company_ids:
            #yield (self.db_connector.read_company_info(company_id[0]), company_id[1])
            yield company_id

    def get_exclude_company_data(self):
        exclude_company_ids =  self.db_connector.read_exclude_new_company()
        for company_id in exclude_company_ids:
            #yield (self.db_connector.read_company_info(company_id[0]), 0)
            yield company_id

    def get_include_company_data_all(self):
        include_company_ids =  self.db_connector.read_include_all_company()
        for company_id in include_company_ids:
            #yield (self.db_connector.read_company_info(company_id[0]), company_id[1])
            yield company_id

    def get_exclude_company_data_all(self):
        exclude_company_ids =  self.db_connector.read_exclude_all_company()
        for company_id in exclude_company_ids:
            #yield (self.db_connector.read_company_info(company_id[0]), 0)
            yield company_id

    def write_insert_file(self, id_generator, name=''):
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        file_name = self.path + name + time_str + 'insert.txt'
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                while True:
                    id_group = self.get_id_group(id_generator)
                    if id_group == []:
                        break
                    company_group = self.db_connector.read_company_info(id_group)
                    for i in range(len(company_group)):
                        #print(company_group[i])
                        print(type(i))
                        data = self.generate_insert_sql(company_group[i])
                        f.write(data)
        except Exception as e:
            print(e)
            print(f'save file failed: {file_name}')
        else:
            print(f'save to path {file_name}')

    def write_update_file(self, id_generator, name=''):
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        file_name = self.path + name + time_str +'update.txt'
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                while True:
                    id_group = self.get_id_group(id_generator)
                    if id_group == []:
                        break
                    company_group = self.db_connector.read_company_info(id_group)
                    for i in range(len(company_group)):
                        print(type(i))
                        data = self.generate_update_sql(company_group[i], id_group[i][1])
                        f.write(data)
        except Exception as e:
            print(e)
            print(f'save file failed: {file_name}')
        else:
            print(f'save to path {file_name}')

    def company_info_to_dict(self, company_info):
        try:
            company_info = dict(zip(self.company_template, company_info))
        except:
            print('can not find company')
            company_info = None
        return company_info

    def generate_insert_sql(self, company_info):
        ci = self.company_info_to_dict(company_info)
        self.recent_id += 1
        dbdcompaniesid = self.recent_id
        sql_dbdcompanies   = f"INSERT INTO vtiger_dbdcompanies(dbdcompaniesid,dbdcompanies) VALUES('{dbdcompaniesid}','{ci['dbdcompanies']}');"
        sql_dbdcompaniescf = f"INSERT INTO vtiger_dbdcompaniescf(dbdcompaniesid,cf_755,cf_757,cf_763,cf_759,cf_761,cf_809,cf_811,cf_813,cf_815,cf_817,cf_799,cf_801,cf_1995) VALUES('{dbdcompaniesid}','{ci['cf_755']}','{ci['cf_757']}','{ci['cf_763']}','{ci['cf_759']}','{ci['cf_761']}','{ci['cf_809']}','{ci['cf_811']}','{ci['cf_813']}','{ci['cf_815']}','{ci['cf_817']}','{ci['cf_799']}','{ci['cf_801']}','{ci['cf_1995']}');"
        sql_crmentity      = f"INSERT INTO vtiger_crmentity(crmid, description, createdtime, modifiedtime, smownerid, smcreatorid, modifiedby, label, setype ) VALUES('{dbdcompaniesid}', '', NOW(), NOW(), 1, 1, 1, '{ci['dbdcompanies']}', 'DBDCompanies');"
        insert_data = sql_dbdcompanies + '\n' + sql_dbdcompaniescf + '\n' + sql_crmentity + '\n'
        return insert_data
         
    def generate_update_sql(self, company_info, crm_id):
        ci = self.company_info_to_dict(company_info)
        dbdcompaniesid = crm_id
        sql_dbdcompanies   = f"UPDATE vtiger_dbdcompanies SET dbdcompanies = '{ci['dbdcompanies']}' WHERE dbdcompaniesid ='{dbdcompaniesid}';"
        sql_dbdcompaniescf = f"UPDATE vtiger_dbdcompaniescf SET cf_755 = '{ci['cf_755']}',cf_757 = '{ci['cf_757']}',cf_763 = '{ci['cf_763']}',cf_759 = '{ci['cf_759']}',cf_761 = '{ci['cf_761']}',cf_809 = '{ci['cf_809']}',cf_811 = '{ci['cf_811']}',cf_813 = '{ci['cf_813']}',cf_815 = '{ci['cf_815']}',cf_817 = '{ci['cf_817']}',cf_799 = '{ci['cf_799']}',cf_801 = '{ci['cf_801']}',cf_1995 = '{ci['cf_1995']}' WHERE dbdcompaniesid ='{dbdcompaniesid}';"
        sql_crmentity      = f"UPDATE vtiger_crmentity SET modifiedtime =NOW(), label='{ci['dbdcompanies']}' WHERE crmid='{dbdcompaniesid}';"

        insert_data = sql_dbdcompanies + '\n' + sql_dbdcompaniescf + '\n' + sql_crmentity + '\n'
        return insert_data

    def get_id_group(self, id_generator):
        group = []
        for i in range(100):
            try:
                group.append(next(id_generator))
            except StopIteration:
                return group
        return group

