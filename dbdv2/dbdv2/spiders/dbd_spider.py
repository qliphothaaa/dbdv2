import scrapy
import time
#from browser.session_requester import Requester
from data_access.dbd_connector import DbdConnector
from dbdv2.items import Dbdv2Item

DEBUG=False

class DbdSpider(scrapy.Spider):
    name = 'dbdv2'
    
    #cookie = None
    #fake = Requester()
    #cookie = fake.findJsessionID()
    db = DbdConnector()

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    }

    #allowed_domains = ['datawarehouse.dbd.go.th']

    def start_requests(self):
        company_ids = self.db.getCompanyIdList()
        for i in company_ids:
            company_id = i[0]
            url = 'https://datawarehouse.dbd.go.th/company/profile/%s/%s' %(company_id[3],company_id)
            yield scrapy.Request(url, self.parse)
            

    def parse(self, response):
        if DEBUG == True:
            print('the page name is: %s'% response.driver_title)
            print('''
            -------------------------------------
            %s


            -------------------------------------
            '''% response.body)
        

        objective = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[5]/div/p/text()').get()
        if objective == '-':
            objective = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[3]/div/p/text()').get()

        director_list = []
        directors = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/ol/li/text()').getall()
        for i in directors:
            director_list.append(i.strip())

        item = Dbdv2Item()
        #item['success'] = True
        #item['company_id']   = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[1]/div/div[1]/p/text()').get()
        item['company_id'] = response.url.split('/')[-1]
        #item['company_type'] = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[1]/th[2]/text()').get()
        item['company_type'] = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tbody/tr[1]/th[2]/text()').get()
        #item['status']       = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[3]/td[2]/text()').get()
        item['status']       = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tbody/tr[3]/td[2]/text()').get()
        item['objective']    = objective
        item['directors']    = director_list


        return item



