import re
import datetime
def address_separater(s):
    #this method separater the address which from datawarehouse to small part
    province_b    = 'กรุงเทพมหานคร'
    province      = 'จ\\.'

    district_b    = 'เขต'
    district      = 'อ\\.|อำเภอ'

    subdistrict_b = 'แขวง'
    subdistrict   = 'ต\\.|ตำบล'



    #print(s)
    if province_b in s:
        pattern = f'(.*){subdistrict_b}(.*){district_b}(.*){province_b}'
        matchObject = re.match(pattern, s)

        company_street      = matchObject.group(1).strip()
        company_subdistrict = matchObject.group(2).strip()
        company_district    = matchObject.group(3).strip()
        company_province    = province_b
    else:
        pattern = f'(.*)({subdistrict})(.*)({district})(.*){province}(.*)'
        matchObject = re.match(pattern, s)

        company_street      = matchObject.group(1).strip()
        company_subdistrict = matchObject.group(3).strip()
        company_district    = matchObject.group(5).strip()
        company_province    = matchObject.group(6).strip()
        
    return [company_street, company_subdistrict, company_district, company_province]

def address_clear(subdistrict, district, province):
    #this method clear the prefix of the address from excel file
    province_b            = 'กรุงเทพมหานคร'
    province_pattern      = 'จ'

    district_pattern_b    = 'เขต'
    district_pattern      = 'อ|อำเภอ'

    subdistrict_pattern_b = 'แขวง'
    subdistrict_pattern   = 'ต|ตำบล'

    print(subdistrict)

    if province == province_b:
        if district_pattern_b in district:
            district = district[3:]
        if subdistrict_pattern_b in subdistrict:
            subdistrict = subdistrict[4:]
        #district = district.lstrip(district_pattern_b)
        #subdistrict = subdistrict.lstrip(subdistrict_pattern_b)
    else:
        province = province.lstrip(province_pattern).lstrip('.')
        district = district.lstrip(district_pattern).lstrip('.')
        subdistrict = subdistrict.lstrip(subdistrict_pattern).lstrip('.')

    print(subdistrict)
    
    return subdistrict, district, province


def business_type_separater(s):
    #this method separate the type code and type detail
    s = s.strip('"')
    bussiness_type_code = ''
    bussiness_type      = ''
    try:
        matchObject = re.match('([0-9]*)(.*)', s)
        bussiness_type_code = matchObject.group(1).strip()
        bussiness_type      = matchObject.group(2).strip()
    except:
        print('error')

    return (bussiness_type_code, bussiness_type)

def date_convert(time):
    if isinstance(time,str):
        temptime = datetime.datetime.strptime(time_str, '%d/%M/%Y').date()
        temptime = temptime.replace(year = temptime.year-543)
        res = datetime.datetime.strftime(temptime , '%Y-%m-%d')
    elif isinstance(time, datetime.datetime):
        time = time.replace(year = time.year-543)
        res = datetime.datetime.strftime(time, '%Y-%m-%d')
    #print(res)
    return res

'''
    #print(s)
    if province_b in s:
        pattern = f'(.*){subdistrict_b}(.*){district_b}(.*){province_b}'
        matchObject = re.match(pattern, s)

        company_street      = matchObject.group(1).strip()
        company_subdistrict = matchObject.group(2).strip()
        company_district    = matchObject.group(3).strip()
        company_province    = province_b
    else:
        pattern = f'(.*)({subdistrict})(.*)({district})(.*){province}(.*)'
        matchObject = re.match(pattern, s)

        company_street      = matchObject.group(1).strip()
        company_subdistrict = matchObject.group(3).strip()
        company_district    = matchObject.group(5).strip()
        company_province    = matchObject.group(6).strip()
        
    return [company_subdistrict, company_district, company_province]
'''
if __name__ == "__main__":
    strings = ['857 ซอยเพชรเกษม94 แขวงบางแคเหนือ เขตบางแค กรุงเทพมหานคร', '39 หมู่ที่ 5 ต.นิคมพัฒนา อ.นิคมพัฒนา จ.ระยอง', '122/2หมู่ที่12 ตำบลสันกำแพงอำเภอสันกำแพงจ.เชียงใหม่']

    for string in strings:
        address = address_separater(string)
        print(f'raw address:{address}')
        print(f'address with header:{address_decorator(address)}')
