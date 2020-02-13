import scrapy
import time
from data_access.dbd_connector import DbdConnector
from dbdv2.items import AnnuallyItem

class AnnuallySpider(scrapy.Spider):
    name = 'annually'
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
        company_ids = db.getAllCompanyIdList()
        if len(company_ids) > 0:
            print("======================Strat scraping! There are %d company in schedule=================" % len(company_ids))
        else:
            print("======================no company in schedule!====================")

        for i in company_ids:
            company_id = i[0]
            url = 'https://datawarehouse.dbd.go.th/company/profile/%s/%s' %(company_id[3],company_id)
            yield scrapy.Request(url, self.parse)


    def parse(self, response):

        company_name = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[1]/h2/text()').get()

        objective = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[5]/div/p/text()').get()
        if objective == '-':
            objective = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[3]/div/p/text()').get()


        director_list = []
        directors = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/ol/li/text()').getall()
        for i in directors:
            director_list.append(i.strip())

        raw_bussiness_type = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[4]/div/p/text()').get().strip()
        if raw_bussiness_type == '-':
            raw_bussiness_type = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/div/p/text()').get().strip()

        item = AnnuallyItem()
        item['scraping_status'] = response.request.status
        item['company_id']     = response.url.split('/')[-1]
        item['company_type']   = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tbody/tr[1]/th[2]/text()').get()
        item['status']         = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tbody/tr[3]/td[2]/text()').get()
        item['address']        = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[2]/td/text()').get()
        item['company_name']   = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[1]/h2/text()').get()
        item['objective']      = objective
        item['directors']      = director_list
        item['bussiness_type'] = raw_bussiness_type


        return item
