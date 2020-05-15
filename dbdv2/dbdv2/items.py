# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MonthlyItem(scrapy.Item):
    scraping_status = scrapy.Field()
    company_id      = scrapy.Field()
    company_name    = scrapy.Field()
    company_type    = scrapy.Field()
    status          = scrapy.Field()
    objective       = scrapy.Field()
    directors       = scrapy.Field()
    bussiness_type  = scrapy.Field()
    address         = scrapy.Field()

class FailedItem(scrapy.Item):
    scraping_status = scrapy.Field()
    found           = scrapy.Field()
    company_id      = scrapy.Field()

class AnnuallyItem(scrapy.Item):
    scraping_status = scrapy.Field()
    company_id      = scrapy.Field()
    company_name    = scrapy.Field()
    company_type    = scrapy.Field()
    status          = scrapy.Field()
    objective       = scrapy.Field()
    directors       = scrapy.Field()
    bussiness_type  = scrapy.Field()
    address         = scrapy.Field()



