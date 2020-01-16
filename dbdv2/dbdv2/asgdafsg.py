import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class Requester(object):
    def __init__(self, session=''):
        self.setUpDriver()
        self.session = session


    def setUpDriver(self):
        options = Options()
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        options.add_argument('--lang=en')
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')
        self.driver = webdriver.Chrome(chrome_options=options)

        name = 'JSESSIONID'
        value = 'MTg4N2ViOGMtNWU5ZS00ZTAzLWFjYTMtMzEzYzE5ZjhkYmVj'
        domain = 'datawarehouse.dbd.go.th'

        self.driver.get('https://datawarehouse.dbd.go.th/index')
        self.driver.add_cookie({'name' : name, 'value' : value, 'domain': domain, 'path':'/' })



    def get(self, company_id):
#driver.get('https://datawarehouse.dbd.go.th/login')
        self.driver.get('https://datawarehouse.dbd.go.th/index')
        self.driver.find_element_by_xpath('//*[@id="textStr"]').send_keys(company_id)
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="textStr"]').send_keys(u'\ue007')
        self.driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr/td[1]').click()
        return self.driver

        #return HtmlResponse(driver.current_rul, body=driver.page_source, encoding='utf-8', requester=request)



#driver.get('https://datawarehouse.dbd.go.th/company/profile/5/0105554123553')



    '''
    if 'Error' in driver.title:
        print('failed')
        print('url: %s'% driver.current_url)
        print(driver.title)
        time.sleep(5)
    else:
        print('success')
        print(driver.title)
        time.sleep(5)

    driver.quit()
    '''
