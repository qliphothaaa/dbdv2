from data_access.rex import *
import unittest

class TestRegularExpression(unittest.TestCase):
    def test_address_separater(self):
        address_bangkok = '857 ซอยเพชรเกษม94 แขวงบางแคเหนือ เขตบางแค กรุงเทพมหานคร'
        separeted_address = address_separater(address_bangkok)
        self.assertEqual(separeted_address[0], '857 ซอยเพชรเกษม94')
        self.assertEqual(separeted_address[1], 'บางแคเหนือ')
        self.assertEqual(separeted_address[2], 'บางแค')
        self.assertEqual(separeted_address[3], 'กรุงเทพมหานคร')
        
        address_normal = '39 หมู่ที่ 5 ต.นิคมพัฒนา อ.นิคมพัฒนา จ.ระยอง'
        separeted_address = address_separater(address_normal)
        self.assertEqual(separeted_address[0], '39 หมู่ที่ 5')
        self.assertEqual(separeted_address[1], 'นิคมพัฒนา')
        self.assertEqual(separeted_address[2], 'นิคมพัฒนา')
        self.assertEqual(separeted_address[3], 'ระยอง')
        
    def test_address_clear(self):
        address_bangkok = ['แขวงคลองสองต้นนุ่น', 'เขตลาดกระบัง', 'กรุงเทพมหานคร']
        cleared_address = address_clear(*address_bangkok)
        self.assertEqual(cleared_address[0], 'คลองสองต้นนุ่น')
        self.assertEqual(cleared_address[1], 'ลาดกระบัง')
        self.assertEqual(cleared_address[2], 'กรุงเทพมหานคร')


        address_normal = ['ต.บางรักน้อย','อ.เมืองนนทบุรี','จ.นนทบุรี']
        cleared_address = address_clear(*address_normal)
        self.assertEqual(cleared_address[0], 'บางรักน้อย')
        self.assertEqual(cleared_address[1], 'เมืองนนทบุรี')
        self.assertEqual(cleared_address[2], 'นนทบุรี')

    def test_business_type_separater(self):
        type_info = '68103 การเช่าและการดำเนินการเกี่ยวกับอสังหาริมทรัพย์ที่เป็น ของตนเองหรือเช่าจากผู้อื่นเพื่อเป็นที่พักอาศัย'
        type_info_separated = business_type_separater(type_info)
        self.assertEqual(type_info_separated[0], '68103')
        self.assertEqual(type_info_separated[1], 'การเช่าและการดำเนินการเกี่ยวกับอสังหาริมทรัพย์ที่เป็น ของตนเองหรือเช่าจากผู้อื่นเพื่อเป็นที่พักอาศัย')


