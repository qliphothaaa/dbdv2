import os, time, re, pickle, signal
 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .captcha_reader import readCaptcha

class Browser(object):
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
        self.driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)
        self.driver.set_page_load_timeout(10)

        self.cookie_path = 'cookie.txt'
        self.screenshot_path =  'screenshot.png'
        self.target_captcha_url = 'https://datawarehouse.dbd.go.th/index'


    def initPage(self):
        print('init browser success')
        self.driver.get(self.target_captcha_url)#get the home page
        #self.driver.get('https://www.google.com')#get the home page
        print('finish get the page')


    def setCookie(self):
        self.driver.delete_all_cookies()

        cookie = self.getCookieFromFile()
        if cookie and self.checkCookie(cookie):
            print('cookie worked')
        else:
            cookie = self.getCookieFromWeb()
            if cookie:
                self.driver.add_cookie(cookie)
        print(cookie)

    def getCookieFromFile(self):

        cookies = None
        if os.path.isfile(self.cookie_path):
            try:
                with open(self.cookie_path, 'rb') as f: 
                    cookies = pickle.load(f)
            except EOFError:
                cookies = None

        if cookies:
            for i in cookies:
                if i['name']== 'JSESSIONID':
                    #print(i)
                    return i
        return ''


    def getCookieFromWeb(self):
        print("%%%%start get cookie from website")
        self.driver.get('https://datawarehouse.dbd.go.th/login')
        #self.driver.get('https://www.google.com')
        print(self.driver.get_cookies())
        for i in range(5):
            time.sleep(2)
            captcha_str = self.getCaptcha()
            if len(captcha_str) < 5 or not re.match('^[A-Za-z0-9]+$',captcha_str): 
                #self.driver.close()
                self.driver.refresh()
                #print('fail to read captcha')
                continue
            self.driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(captcha_str) 
            self.driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(u'\ue007') 
            if 'Home' in self.driver.title: 
                #print('successfully read captcha')
                break
            #print('wrong captcha, try again...')

        cookies = self.driver.get_cookies()


        for i in cookies:
            print(i)
            if i['name'] == 'JSESSIONID':
                with open('cookie.txt', 'wb') as f:
                    pickle.dump(cookies, f)
                    #print('renew cookie file')
                return i

        return ''
            
        


    def getCaptcha(self):
        print("%%%%start read captcha")
        self.driver.save_screenshot(self.screenshot_path)
        captcha_str = readCaptcha(self.screenshot_path)[0:5]
        print('captcha string is: '+captcha_str)
        return captcha_str


    def checkCookie(self, cookie):
        print("%%%%start check cookie")
        #self.driver.get('https://datawarehouse.dbd.go.th/index')
        self.driver.get(self.target_captcha_url)
        self.driver.add_cookie(cookie)
        self.driver.get(self.target_captcha_url)
        if 'Error' in self.driver.title:
            print('the cookie is expired')
            self.driver.delete_all_cookies()
            return False
        else:
            return True



    def getPage(self, url):
        try:
            self.driver.get(url)
            page = self.driver.page_source
            title = self.driver.title
            #self.driver.close()
        except TimeoutException as e:
            page = ''
            title = ''
        return (page, title)



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
            pass
        #print('finish close driver')


if __name__ == "__main__":
    a = Browser()
    try:
        a.setCookie()
    finally:
        a.close()

