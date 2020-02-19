import re
def address_separater(s):
    province_b    = 'กรุงเทพมหานคร'
    province      = 'จ\\.'

    district_b    = 'เขต'
    district      = 'อ\\.|อำเภอ'

    subdistrict_b = 'แขวง'
    subdistrict   = 'ต\\.|ตำบล'



    print(s)
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
    province_b    = 'กรุงเทพมหานคร'
    province_pattern      = 'จ.'

    district_pattern_b   = 'เขต'
    district_pattern      = 'อ.|อำเภอ'

    subdistrict_pattern_b = 'แขวง'
    subdistrict_pattern   = 'ต.|ตำบล'

    if province == province_b:
        district = district.lstrip(district_pattern_b)
        subdistrict = subdistrict.lstrip(subdistrict_pattern_b)
    else:
        province = province.lstrip(province_pattern)
        district = district.lstrip(district_pattern)
        subdistrict = subdistrict.lstrip(subdistrict_pattern)
    return subdistrict, district, province

    print(s)
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

def business_type_separater(s):
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

if __name__ == "__main__":
    strings = ['857 ซอยเพชรเกษม94 แขวงบางแคเหนือ เขตบางแค กรุงเทพมหานคร', '39 หมู่ที่ 5 ต.นิคมพัฒนา อ.นิคมพัฒนา จ.ระยอง', '122/2หมู่ที่12 ตำบลสันกำแพงอำเภอสันกำแพงจ.เชียงใหม่']

    for string in strings:
        address = address_separater(string)
        print(f'raw address:{address}')
        print(f'address with header:{address_decorator(address)}')
