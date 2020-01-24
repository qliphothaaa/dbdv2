import unittest
from data_access.xls_reader import DbdExcelReader

class TestExcelReader(unittest.TestCase):
    def setUp(self):
        self.excelReader = DbdExcelReader('tests/test_data/99_201903.xls', 10)

    def test_readExcel(self):
        self.excelReader.readExcel()
        self.assertEqual(list(self.excelReader.data_dict.columns),["ROW","ID", "NAME_TH", "REGISTRATION_DATE", "REGISTRATION_MONEY", "BUSINESS_TYPE_CODE", "BUSINESS_TYPE", "STREET", "SUBDISTRICT", "DISTRICT", "PROVINCE", "ZIPCODE"])


    def test_hanldeData(self):
        self.excelReader.readExcel()
        self.assertEqual(list(self.excelReader.data_dict.columns),["ROW","ID", "NAME_TH", "REGISTRATION_DATE", "REGISTRATION_MONEY", "BUSINESS_TYPE_CODE", "BUSINESS_TYPE", "STREET", "SUBDISTRICT", "DISTRICT", "PROVINCE", "ZIPCODE"])

        self.excelReader.hanldeData()
        self.assertEqual(list(self.excelReader.data_dict.columns),["ROW","ID", "NAME_TH", "REGISTRATION_DATE", "REGISTRATION_MONEY", "BUSINESS_TYPE_CODE", "BUSINESS_TYPE", "STREET", "SUBDISTRICT", "DISTRICT", "PROVINCE", "ZIPCODE", "ADDRESS"])

        for i in range(10):
            self.assertEqual(self.excelReader.data_dict.iloc[i]["ADDRESS"], self.excelReader.data_dict.iloc[i]["STREET"] + ' ' + self.excelReader.data_dict.iloc[i]["SUBDISTRICT"])
    









if __name__ == "__main__":
    unittest.main()
