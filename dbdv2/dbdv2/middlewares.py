import time
import os.path
from scrapy import signals
from scrapy.http import HtmlResponse
#from scrapy.exceptions import CloseSpider
from browser.scraping_browser import ScrapingBrowser


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
    def __init__(self):
        self.fake_browser  = ScrapingBrowser()
        self.success_count = 0
        self.fail_count    = 0


    def __del__(self):

        print("Downloader(finished): finish scraping, Totally %d companys, %d data completed, %d data failed==========" %(self.success_count + self.fail_count, self.success_count, self.fail_count))
        self.fake_browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        print("Downloader: get page of company No.%d " % (self.success_count + self.fail_count + 1))
        
        time.sleep(1)

        page, title, code = self.fake_browser.getPage(request.url)

        #request.driver_title = title

        #if the title exist, mean the get page succeed
        if title:
            print("Downloader: Successfully got page of company No.%d " % (self.success_count + self.fail_count + 1))
            self.success_count += 1
            request.status = True
        else:
            print("Downloader: Fail to Get page of company No.%d" % (self.success_count + self.fail_count + 1))
            self.fail_count += 1
            request.status = False


        if code == '404':
            #if the company cannot be found
            print('Downloader: cannot find the page in datawarehouse')
            pass
        elif code == '':
            print('Downloader: find page time out!')
            #if timeout
            pass
        elif code == '401':
            #if cookie died
            #raise CloseSpider('@@@@@@@@@@@@@@@the cooike expired in scraping@@@@@@@@@@@@@@@@')
            print('Downloader: cookie expired!')
            spider.close_it = 'cookie expired!'

        elif  code == '500' or code == '503' or code == '000':
            #if the server down:500, 503
            #or some error system does not know: 000

            #self.fake_browser.driver.save_screenshot('failed.png')
            #raise CloseSpider('@@@@@@@@@@@@@@@@@@@@the server is down! Please try to run it later@@@@@@@@@@@@@@@@@')
            print(f'Downloader: server is down! code{code}')
            spider.close_it = f'server is down! code{code}'
        else:
            #spider.close_it = 'nothing I just want to see'
            pass

        response = HtmlResponse(url=request.url, body=page, request=request, encoding='utf-8')
        return response
        #return None

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
