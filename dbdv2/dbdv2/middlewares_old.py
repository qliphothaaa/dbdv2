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

from captcha.captcha_reader import readCaptcha


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
        #CHROME_BIN = "/usr/bin/chromium"
        #CHROME_DRIVER = os.path.expanduser('/usr/bin/chromedriver')
        chrome_options = Options()
        #chrome_options.binary_location = CHROME_BIN
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36')

        #self.driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        

        self.driver.get('https://datawarehouse.dbd.go.th/index')#get the home page, the driver need to access the page first then set cookie
        #self.driver.get('www.google.com')#get the home page, the driver need to access the page first then set cookie
        cookie = self.findJsessionID()

        #for i in cookie:
            #self.driver.add_cookie(i)
        self.driver.add_cookie(cookie[2])



    def __del__(self):
        self.driver.quit()
        #print('++++++++++++++++quit driver')


    def findJsessionID(self):
        cookie = self.getCookieFromFile()

        if cookie == '':
            print('no cookie in local, try to get it from website')
            cookie = self.getCookieFromWeb()
        else:
            print('the local cookie is ok! start to scrapy')

        return cookie

    def getCookieFromWeb(self):
        for i in range(5):
            time.sleep(2)
            captcha_str = self.getCaptcha()         #read the captcha
            if len(captcha_str) < 5 or not re.match('^[A-Za-z0-9]+$',captcha_str): #if the string length is less then 5 or have special character, read it again
                self.driver.get('https://datawarehouse.dbd.go.th/login')#get the home page again
                print('fail to read captcha')
                continue
            self.driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(captcha_str) #input the captcha string
            #time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(u'\ue007') #press enter key
            if 'Home' in self.driver.title: #if the home in title,it mean the captcha is correct
                print('successfully read captcha')
                break
            print('wrong captcha, try again...')

        #print('the page title is: '+self.driver.title)
        #self.driver.save_screenshot('re.png')
        cookie = self.driver.get_cookies()
        if cookie is not None:
            with open('./captcha/cookie.txt', 'wb') as f:
                pickle.dump(cookie, f)
                print('renew cookie file')
        return cookie

    def getCookieFromFile(self):
        cookie = ''
        path = './captcha/cookie.txt'
        if os.path.isfile(path):
            print('file exist')
        else:
            print('no cookie file')
            open(path, 'a').close()
        #this check the file is empty or not
        with open(path, 'rb') as f: 
            f.seek(0)
            first_char = f.read(1)
            if first_char:
                f.seek(0)
                cookie = pickle.load(f)
                print('load cookie from file')

        #if cookie is not empty, use the cookie to access page for checking the cookie
        if cookie is not '':
            print('cookie exist, check it now')
            for i in cookie:
                self.driver.add_cookie(i)
            self.driver.get('https://datawarehouse.dbd.go.th/index')#get the home page
            print(self.driver.title)
            if 'Error' in self.driver.title:
                cookie = '' #if the cookie is expired, set the cookie to empty

        return cookie

    def getCaptcha(self):
        path = './captcha/screenshot.png'
        self.driver.save_screenshot(path)
        captcha_str = readCaptcha(path)[0:5]
        print('captcha string is: '+captcha_str)
        return captcha_str



    ###############################

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        #time.sleep(2)
        self.driver.get(request.url)
        request.driver_title = self.driver.title
        response = HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8')#, status=200)

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
