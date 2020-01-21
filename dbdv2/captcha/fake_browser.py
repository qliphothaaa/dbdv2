import os, time, re, pickle, signal
 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .captcha_reader import readCaptcha
 

class Browser(object):
    def __init__(self):
        CHROME_BIN = "/usr/bin/chromium"
        CHROME_DRIVER = os.path.expanduser('/usr/bin/chromedriver')
        chrome_options = Options()
        chrome_options.binary_location = CHROME_BIN
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36')

        self.driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)
        print('init browser success')
        self.driver.get('https://datawarehouse.dbd.go.th/index')#get the home page
        #self.driver.get('https://www.google.com')#get the home page
        print('finish get the page')

    def setCookie(self):
        cookie = self.getCookieFromFile()
        if not cookie:
            cookie = self.getCookieFromWeb()
        print(cookie)



    def getCookieFromFile(self):
        cookie = ''
        path = 'cookie.txt'
        if os.path.isfile(path):
            print('file exist')
            with open(path, 'rb') as f: 
                f.seek(0)
                first_char = f.read(1)
                if first_char:
                    f.seek(0)
                    cookie = pickle.load(f)
                    print('load cookie from file')
        else:
            print('no cookie file')
            open(path, 'a').close()

        if cookie is not '':
            print('cookie exist, check it now')
            for i in cookie:
                if i['name']== 'JSESSIONID':
                    print(i)
                    self.driver.add_cookie(i)
            self.driver.get('https://datawarehouse.dbd.go.th/index')
            print(self.driver.title)
            if 'Error' in self.driver.title:
                print('the cookie is expired')
                cookie = '' 
                self.driver.delete_all_cookies()
        return cookie


    def getCookieFromWeb(self):
        self.driver.get('https://datawarehouse.dbd.go.th/login')
        for i in range(5):
            time.sleep(2)
            captcha_str = self.getCaptcha()
            if len(captcha_str) < 5 or not re.match('^[A-Za-z0-9]+$',captcha_str): 
                self.driver.get('https://datawarehouse.dbd.go.th/login')
                print('fail to read captcha')
                continue
            print('XXXXXXXXXXXXX here come?')
            self.driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(captcha_str) 
            print('XXXXXXXXXXXXX here come?22')
            self.driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(u'\ue007') 
            print('XXXXXXXXXXXXX here come?222')
            if 'Home' in self.driver.title: 
                print('successfully read captcha')
                break
            print('wrong captcha, try again...')

        cookie = self.driver.get_cookies()
        if cookie is not None:
            with open('cookie.txt', 'wb') as f:
                pickle.dump(cookie, f)
                print('renew cookie file')
        return cookie


    def getCaptcha(self):
        path = 'screenshot_l.png'
        self.driver.save_screenshot(path)
        captcha_str = readCaptcha(path)[0:5]
        print('captcha string is: '+captcha_str)
        return captcha_str

    def getPage(self, url):
        self.driver.get(url)
        page = self.driver.page_source
        title = self.driver.title
        #self.driver.close()
        return (page, title)



    def close(self):
        pid = self.driver.service.process.pid
        print('start to close tabs')
        self.driver.close()
        print('start to close driver'+ str(pid))
        #self.driver.quit()
        try:
            os.kill(int(pid), signal.SIGTERM)
            print("killed the chrome using process")
        except ProcessLookupError as ex:
            print(ex)
            pass
        print('finish close driver')

if __name__ == "__main__":
    a = Browser()
    a.setCookie()
    a.close()

