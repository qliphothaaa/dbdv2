import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
#options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

driver.get('https://www.google.co.jp/')
print(driver.title)

'''
assert 'Google' in driver.title

input_element = driver.find_element_by_name('q')
input_element.send_keys('Python')
input_element.send_keys(Keys.RETURN)

time.sleep(2)  # Chromeの場合はAjaxで遷移するので、とりあえず適当に2秒待つ。

assert 'Python' in driver.title

driver.save_screenshot('search_results.png')

for a in driver.find_elements_by_css_selector('h3 > a'):
    print(a.text)
    print(a.get_attribute('href'))
'''

driver.quit()  # ブラウザーを終了する。

