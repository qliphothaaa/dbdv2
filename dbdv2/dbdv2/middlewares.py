# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import time, re, pickle
import os.path
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from captcha.fake_browser import Browser


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
        print('=============init middleware')
        self.fake_browser = Browser()
        self.fake_browser.setCookie()



    def __del__(self):
        self.fake_browser.close()
        #print('++++++++++++++++quit driver')



    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        time.sleep(2)
        #self.driver.get(request.url)
        page, title = self.fake_browser.getPage(request.url)
        request.driver_title = title
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
