import scrapy
import time
from data_access.dbd_connector import DbdConnector
from dbdv2.items import AnnuallyItem, FailedItem
from scrapy.exceptions import CloseSpider

class AnnuallySpider(scrapy.Spider):
    name = 'annually'
    close_it = ''
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    }
    allowed_domains = ['datawarehouse.dbd.go.th']

    custom_settings = {
        'ITEM_PIPELINES':{
            'dbdv2.pipelines.AnnuallyScrapingtPipeline': 500,
        }
    }

    def start_requests(self):
        db = DbdConnector()

        #check it is retry or not
        if int(self.retry) == 0:
            db.clear_status_before_annually()
            try:
                self.start = int(self.start)
                self.end =  int(self.end)
                if self.start>self.end:
                    self.end = self.start
                query = f'select DBD_COMPANY_ID from dbd_query limit {self.start-1},{self.end-self.start+1}'
                print(query)
            except Exception as e:
                print(e)
                query = 'select DBD_COMPANY_ID from dbd_query'
            print(query)
            company_ids = db.readIds(query)
        elif int(self.retry) == 1:
            query = 'select DBD_COMPANY_ID from dbd_query where DBD_STATUS is Null'
            company_ids = db.readIds(query)
            query = 'select DBD_COMPANY_ID from dbd_query where DBD_STATUS = "Failed"'
            company_ids2 = db.readIds(query)
            company_ids.extend(company_ids2)
        db.dbClose()

        if len(company_ids) > 0:
            print("======================Strat scraping! There are %d company in schedule=================" % len(company_ids))
        else:
            print("======================no company in schedule!====================")

        for i in company_ids:
            company_id = i[0]
            url = 'https://datawarehouse.dbd.go.th/company/profile/%s/%s' %(company_id[3],company_id)
            yield scrapy.Request(url, self.parse)


    def parse(self, response):
        if self.close_it:
            #print(self.close_it)
            raise CloseSpider(self.close_it)

        company_id = response.url.split('/')[-1]

        #print('23145677456'  + str(response.request.status))

        if response.request.status:
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
                #print("this company didn't update type")
                raw_bussiness_type = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/div/p/text()').get().strip()
            #else:
                #print('this company update his type')

            item = AnnuallyItem()
            item['scraping_status'] = response.request.status
            #item['company_id']     = response.url.split('/')[-1]
            item['company_id']     = company_id
            item['company_type']   = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[1]/th[2]/text()').get()
            item['status']         = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[3]/td[2]/text()').get()
            item['address']        = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/table/tr[2]/td/text()').get()
            item['company_name']   = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[1]/h2/text()').get()
            item['objective']      = objective
            item['directors']      = director_list
            item['bussiness_type'] = raw_bussiness_type
            return item

        else:
            item = FailedItem()
            item['scraping_status'] = False
            item['company_id'] = company_id
            print('failed item '+company_id)
            return item
