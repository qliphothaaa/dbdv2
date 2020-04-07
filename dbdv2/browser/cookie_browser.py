import os, time, re, pickle, signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pytesseract
from PIL import Image


class CookieBrowser(object):
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
        self.driver.set_page_load_timeout(30)

        self.cookie_path = 'browser/temp/cookie.txt'
        self.screenshot_path =  'browser/temp/screenshot.png'
        self.target_captcha_url = 'https://datawarehouse.dbd.go.th/index'


    def initPage(self):
        print('init browser success')
        self.driver.get(self.target_captcha_url)#get the home page
        print('finish get the page')


    def downloadCookie(self):
        self.driver.delete_all_cookies()

        cookie = self.getCookieFromFile()
        if cookie and self.checkCookie(cookie):
            print('local cookie worked')
        else:
            print('local cookie expired')
            cookie = self.getCookieFromWeb()
            if cookie:
                print('local cookie renew')
            else:
                print('no cookie! look like the getcaptcha program have some problem!')
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
        print(self.driver.get_cookies())
        for i in range(10):
            time.sleep(2)
            captcha_str = self.getCaptcha()
            if len(captcha_str) < 5 or not re.match('^[A-Za-z0-9]+$',captcha_str): 
                self.driver.refresh()
                continue
            self.driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(captcha_str) 
            self.driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(u'\ue007') 
            if 'Home' in self.driver.title: 
                break

        cookies = self.driver.get_cookies()


        for i in cookies:
            print(i)
            if i['name'] == 'JSESSIONID':
                with open(self.cookie_path, 'wb') as f:
                    pickle.dump(cookies, f)
                return i
            else:
                print('no JSESSIONID in this page!')

        return ''


    def getCaptcha(self):
        #print("%%%%start read captcha")
        self.driver.save_screenshot(self.screenshot_path)
        captcha_str = readCaptcha(self.screenshot_path)[0:5]
        #print('captcha string is: '+captcha_str)
        return captcha_str


    def checkCookie(self, cookie):
        print("%%%%start check cookie")
        #self.driver.get('https://datawarehouse.dbd.go.th/index')
        self.driver.get(self.target_captcha_url)
        self.driver.add_cookie(cookie)
        time.sleep(5)
        self.driver.get(self.target_captcha_url)
        if 'Error' in self.driver.title:
            print('the cookie is expired')
            self.driver.delete_all_cookies()
            return False
        else:
            return True
        
    def readCaptcha(self,img_path):
        result = ''

        try:
            screen = Image.open(img_path)
        except:
            print('no Image')
            return result

        width, height = screen.size
        captcha = screen.crop((370/1600*width, 1120/1200*height, 600/1600*width, height))
        captcha = captcha.convert('RGB')
        color = captcha.getpixel((2,2))
        width, height = captcha.size
        pixels = captcha.load()
        for i in range(width):
            for j in range(height):
                if pixels[i, j] != color:
                    pixels[i, j] = (0,0,0)
                else:
                    pixels[i, j] = (255,255,255)

        result = pytesseract.image_to_string(captcha, lang='eng', config='--dpi 100 --psm 7')

        return result



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
    a = CookieBrowser()
    try:
        a.downloadCookie()
    finally:
        a.close()

