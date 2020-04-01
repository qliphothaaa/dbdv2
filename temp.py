    def write_update_file(self, id_generator):
        file_name = self.path + time_str +'update.txt'
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                while True:
                    id_group = self.get_id_group(id_generator)
                    if id_group == []:
                        break
                    company_group = self.db_connector.read_company_info(id_group)
                    for i in range(len(company_group)):
                        #print(type(i))
                        data = self.generate_update_sql(company_group[i], id_group[i][1])
                        f.write(data)
        except Exception as e:
            print(e)
            print(f'save file failed: {file_name}')
        else:
            print(f'save to path {file_name}')



    def write_file(self, id_generator):
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        file_count = 1
        finished = False

        try:

            while not finished:
                file_name = self.path + time_str + f'update{file_count}.txt'
                row_count = 0
                with open(file_name, 'w', encoding='utf-8') as f:
                    while True:
                        id_group = self.get_id_group(id_generator)
                        if id_group = []:
                            finished = True
                            break
                        else:
                            company_group = self.db_connector.read_company_info(id_group)

                        for i in range(len(company_group)):
                            data = self.generate_update_sql(company_group[i], id_group[i][1])
                            f.write(data)
                        row_count += 100

                        if row_count >= 100000:
                            file_count += 1
                            break

        except Exception as e:
            print(e)
            print(f'save file failed: {file_name}')
        else:
            print(f'save to path {file_name}')




