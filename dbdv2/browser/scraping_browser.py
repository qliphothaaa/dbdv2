import os, time, re, pickle, signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .captcha_reader import readCaptcha

class ScrapingBrowser(object):
    def __init__(self):
        #print('init driver')
        CHROME_BIN = "/usr/bin/chromium"
        CHROME_DRIVER = os.path.expanduser('/usr/bin/chromedriver')
        chrome_options = Options()
        chrome_options.binary_location = CHROME_BIN
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36')
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        self.driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)
        self.driver.set_page_load_timeout(20)

        self.cookie_path = 'browser/temp/cookie.txt'
        self.screenshot_path =  'browser/temp/screenshot.png'
        self.target_captcha_url = 'https://datawarehouse.dbd.go.th/index'
        self.initPage()


    def initPage(self):
        self.driver.get(self.target_captcha_url)#get the home page

        if os.path.isfile(self.cookie_path):
            try:
                with open(self.cookie_path, 'rb') as f: 
                    cookies = pickle.load(f)
            except EOFError:
                cookies = None
        if cookies:
            for i in cookies:
                if i['name']== 'JSESSIONID':
                    self.driver.add_cookie(i)

        #print('finish init the page')


    def getPage(self, url):
        try:
            self.driver.get(url)
            page = self.driver.page_source
            title = self.driver.title
            error_code = '200'
            if 'Error' in title:
                time.sleep(2)
                self.driver.save_screenshot('browser/temp/error.png')
                error_code = self.driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/div/div[2]/div/h5').text
                title = ''
                page = ''
        except TimeoutException as e:
            page = ''
            title = ''
        return (page, title, error_code)



    def close(self):
        pid = self.driver.service.process.pid
        #print('start to close tabs')
        #print('start to close driver'+ str(pid))
        try:
            self.driver.close()
            os.kill(int(pid), signal.SIGTERM)
            #print("killed the chrome using process")
        except ProcessLookupError as ex:
            print(ex)
        #print('finish close driver')

