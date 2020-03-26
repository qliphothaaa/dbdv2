import scrapy
import time
from data_access.dbd_connector import DbdConnector
from dbdv2.items import MonthlyItem, FailedItem
from scrapy.exceptions import CloseSpider


class DbdSpider(scrapy.Spider):
    name = 'monthly'
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
        if int(self.retry) == 0:
            query = 'select DBD_COMPANY_ID from dbd_new_query Where DBD_STATUS is NULL'
            company_ids = db.readIds(query)
        elif int(self.retry) == 1:
            query = 'select DBD_COMPANY_ID from dbd_new_query Where DBD_STATUS = "Failed"'
            company_ids = db.readIds(query)
            query = 'select DBD_COMPANY_ID from dbd_new_query Where DBD_STATUS is NULL'
            company_ids2 = db.readIds(query)
            company_ids.extend(company_ids2)

        db.dbClose()
        if len(company_ids) > 0:
            print(f"======================Start scraping! There are {len(company_ids)} company in schedule=================")
        else:
            print("======================Start scraping! no company in schedule! All data are complete====================")

        for i in company_ids:
            company_id = i[0]
            url = f'https://datawarehouse.dbd.go.th/company/profile/{company_id[3]}/{company_id}' 
            yield scrapy.Request(url, self.parse)
            

    def parse(self, response):
        if self.close_it:
            print(self.close_it)
            raise CloseSpider(self.close_it)
        company_id = response.url.split('/')[-1]

        if response.request.status:
            #print(f'Spider: spider parse start ({company_id})')

            company_name = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[1]/h2/text()').get()
            if not company_name:
                item = FailedItem()
                item['scraping_status'] = False
                item['company_id'] = company_id
                return item

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
                raw_bussiness_type = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/div/p/text()').get().strip()

            item = MonthlyItem()
            item['scraping_status'] = response.request.status
            item['company_id']      = company_id
            item['company_type']    = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[1]/th[2]/text()').get()
            item['status']          = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[3]/td[2]/text()').get()
            item['objective']       = objective
            item['directors']       = director_list
            item['company_name']    = company_name
            item['bussiness_type']  = raw_bussiness_type
            item['address']         = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/table/tr[2]/td/text()').get()
            #print(f'Spider: spider parse end ({company_id})')
            return item

        else:
            item = FailedItem()
            item['scraping_status'] = False
            item['company_id'] = company_id
            return item
