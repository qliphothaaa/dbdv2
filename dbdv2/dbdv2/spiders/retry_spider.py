import scrapy
import time
#from browser.session_requester import Requester
from data_access.dbd_connector import DbdConnector
from dbdv2.items import MonthlyItem, FailedItem
from scrapy.exceptions import CloseSpider


class DbdSpider(scrapy.Spider):
    name = 'retry'
    close_it = ''
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    }
    allowed_domains = ['datawarehouse.dbd.go.th']

    custom_settings = {
        'ITEM_PIPELINES':{
            'dbdv2.pipelines.MonthlyScrapingPipeline': 300,
        }
    }

    def start_requests(self):
        db = DbdConnector()
        query = 'select DBD_COMPANY_ID from dbd_new_query Where DBD_STATUS = "Failed"'
        company_ids = db.readIds(query)
        if len(company_ids) > 0:
            print("======================Strat scraping failed record! There are %d company in schedule=================" % len(company_ids))
        else:
            print("======================no company is failed! All data succeeded=======================================")

        for i in company_ids:
            company_id = i[0]
            url = 'https://datawarehouse.dbd.go.th/company/profile/%s/%s' %(company_id[3],company_id)
            yield scrapy.Request(url, self.parse)
            

    def parse(self, response):
        if self.close_it:
            print(close_it)
            raise CloseSpider(close_it)

        company_id = response.url.split('/')[-1]
        if response.request.status:
            print(f'***************************************spider parse start ({company_id})**************************')

            company_name = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[1]/h2/text()').get()

            objective = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[5]/div/p/text()').get()
            if objective == '-':
                objective = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[3]/div/p/text()').get()

            director_list = []

            directors = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/ol/li/text()').getall()
            for i in directors:
                director_list.append(i.strip())

            raw_bussiness_type = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[4]/div/p/text()').get()

            try:
                raw_bussiness_type = raw_bussiness_type.strip()
            except:
                raw_bussiness_type = 'ERRRRRRRRRRRRRRRRRRRORRRRRRRRRRRRRRRRRRRRRR:' + response.url.split('/')[-1]

            if raw_bussiness_type == '-':
                print("this company didn't update type")
                raw_bussiness_type = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/div/p/text()').get().strip()
            #else:
                #print('this company update his type')

            item = MonthlyItem()
            item['scraping_status'] = response.request.status
            #item['company_id'] = response.url.split('/')[-1]
            item['company_id'] = company_id
            item['company_type'] = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tbody/tr[1]/th[2]/text()').get()
            item['status']       = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tbody/tr[3]/td[2]/text()').get()
            item['objective']    = objective
            item['directors']    = director_list
            item['company_name'] = company_name
            item['bussiness_type'] = raw_bussiness_type
            print('***************************************parse end**************************')
            return item

        else:
            item = FailedItem()
            item['scraping_status'] = False
            item['company_id'] = company_id
            return item
