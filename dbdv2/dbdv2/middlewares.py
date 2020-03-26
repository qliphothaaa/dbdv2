import time
import os.path
import requests
import pickle
import os
from scrapy import signals
from scrapy.http import HtmlResponse
from browser.scraping_browser import ScrapingBrowser
from requests.exceptions import Timeout


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
        self.success_count = 0
        self.fail_count    = 0


    def __del__(self):
        print("Downloader(finished): finish scraping, Totally %d companys, %d data completed, %d data failed==========" %(self.success_count + self.fail_count, self.success_count, self.fail_count))

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        '''
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
        '''
        #load cookie from local
        cookie_path = 'browser/temp/cookie.txt'
        if os.path.isfile(cookie_path):
            try:
                with open(cookie_path, 'rb') as f: 
                    cookies = pickle.load(f)
            except EOFError:
                cookies = None

        cookies = cookies[-1]['value']



        try:
            time.sleep(0.1)
            response = requests.get(request.url, cookies = {'JSESSIONID':cookies}, timeout=10)
        except Timeout:
            print('Get page time out!')
            self.fail_count += 1
            request.status = False
            response = HtmlResponse(url=request.url, body='', request=request, encoding='utf-8')
            return response



        #check the status
        code = response.status_code

        if code == 404:
            #if the company cannot be found
            print('Downloader: cannot find the page in datawarehouse')
            request.status = False
            self.fail_count += 1

        elif code == 200:
            request.status = True
            self.success_count += 1


        elif code == 401:
            #if cookie died
            #raise CloseSpider('@@@@@@@@@@@@@@@the cooike expired in scraping@@@@@@@@@@@@@@@@')
            print('Downloader: cookie expired!')
            spider.close_it = 'cookie expired!'

        elif  code == 500 or code == 503:
            #if the server down:500, 503
            #or some error system does not know: 000

            #self.fake_browser.driver.save_screenshot('failed.png')
            #raise CloseSpider('@@@@@@@@@@@@@@@@@@@@the server is down! Please try to run it later@@@@@@@@@@@@@@@@@')
            print(f'Downloader: server is down! code{code}')
            spider.close_it = f'server is down! code{code}'
        else:
            print(f'Downloader: unexpect error! code {code}')
            spider.close_it = f'unexpect error! code{code}'
            pass


        #create the body of the response to spider
        html = str(response.content,'utf-8')
        page =  html
        response = HtmlResponse(url=request.url, body=page, request=request, encoding='utf-8')

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
