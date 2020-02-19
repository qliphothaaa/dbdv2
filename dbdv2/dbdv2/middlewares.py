import time
import os.path
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.exceptions import CloseSpider

from browser.scraping_browser import ScrapingBrowser
from .errors import  TargetServerDownError, CookieExpiredError


class Dbdv2SpiderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i
        

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Dbdv2DownloaderMiddleware(object):
    #my code
    def __init__(self):
        print('=============init middleware==============')
        self.fake_browser  = ScrapingBrowser()
        print('fin br')
        self.success_count = 0
        self.fail_count    = 0


    def __del__(self):

        print("===============finish scraping, Totally %d companys, %d data completed, %d data failed==========" %(self.success_count + self.fail_count, self.success_count, self.fail_count))
        self.fake_browser.close()



    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        print("@@@@@@@@@@@@@@@@@@@@@@@@get page of company No.%d @@@@@@@@@@@@@@@@@@@@@@@@@" % (self.success_count + self.fail_count + 1))
        

        time.sleep(1)
        page, title, status = self.fake_browser.getPage(request.url)

        request.status = False

        if status == '401':
            self.fail_count += 1
            raise CloseSpider('@@@@@@@@@@@@@@@the cooike expired in scraping@@@@@@@@@@@@@@@@')
        if status == '500' or status == '503':
            #self.fake_browser.driver.save_screenshot('failed.png')
            #print(self.fake_browser.driver.current_url)
            self.fail_count += 1
            raise CloseSpider('@@@@@@@@@@@@@@@@@@@@the server is down! Please try to run it later@@@@@@@@@@@@@@@@@')

        request.driver_title = title
        
        if title:
            print("@@@@@@@@@@@@@@@@@@@@@@@@Successfully got page of company No.%d @@@@@@@@@@@@@@@@@@@@@@@@@" % (self.success_count + self.fail_count + 1))
            self.success_count += 1
            request.status = True
        else:
            print("@@@@@@@@@@@@@@@@@@@@@@@@Get page of company No.%d failed@@@@@@@@@@@@@@@@@@@@@@@@@" % (self.success_count + self.fail_count + 1))
            self.fail_count += 1


        response = HtmlResponse(url=request.url, body=page, request=request, encoding='utf-8')#, status=200)

        return response

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
