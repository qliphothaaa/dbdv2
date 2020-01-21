import os
 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
 
CHROME_BIN = "/usr/bin/chromium"
CHROME_DRIVER = os.path.expanduser('/usr/bin/chromedriver')
 
options = Options()
options.binary_location = CHROME_BIN
options.add_argument('--headless')
options.add_argument('--disable-gpu')
#options.add_argument('--single-process')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=800,600')
 
driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=options)
 
#driver.get("https://datawarehouse.dbd.go.th/login")
driver.get("https://wikiwiki.jp/dolls-fl/")
print(driver.page_source)
driver.quit()