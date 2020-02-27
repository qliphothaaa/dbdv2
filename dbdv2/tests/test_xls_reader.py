import unittest
from data_access.xls_reader import DbdExcelReader

class TestExcelReader(unittest.TestCase):
    def setUp(self):
        self.excelReader = DbdExcelReader('tests/test_data/99_201903.xls', 10)

    def test_readExcel(self):
        self.excelReader.readExcel()
        #print(list(self.excelReader.data_dict.columns))
        self.assertEqual(list(self.excelReader.data_dict.columns),["ROW","ID", "NAME_TH", "REGISTRATION_DATE", "REGISTRATION_MONEY", "BUSINESS_TYPE_CODE", "OBJECTIVE", "STREET", "SUBDISTRICT", "DISTRICT", "PROVINCE", "ZIPCODE"])


    def test_hanldeData(self):
        self.excelReader.readExcel()
        self.assertEqual(list(self.excelReader.data_dict.columns),["ROW","ID", "NAME_TH", "REGISTRATION_DATE", "REGISTRATION_MONEY", "BUSINESS_TYPE_CODE", "OBJECTIVE", "STREET", "SUBDISTRICT", "DISTRICT", "PROVINCE", "ZIPCODE"])

        self.excelReader.hanldeData()
        self.assertEqual(list(self.excelReader.data_dict.columns),["ROW","ID", "NAME_TH", "REGISTRATION_DATE", "REGISTRATION_MONEY", "BUSINESS_TYPE_CODE", "OBJECTIVE", "STREET", "SUBDISTRICT", "DISTRICT", "PROVINCE", "ZIPCODE"])
    


if __name__ == "__main__":
    unittest.main()
