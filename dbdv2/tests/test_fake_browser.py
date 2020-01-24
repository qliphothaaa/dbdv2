import unittest
from captcha.fake_browser import Browser
from selenium.common import exceptions

class TestBrowser(unittest.TestCase):
    def setUp(self):
        self.browser = Browser()

    def tearDown(self):
        self.browser.close()

    def test_getCookieFromFile(self):
        self.browser.cookie_path = 'tests/test_data/cookie_none.txt'
        self.assertEqual(self.browser.getCookieFromFile(),'')

    def test_getCookieFromFile2(self):
        self.browser.cookie_path = 'tests/test_data/cookie.txt'
        cookies = self.browser.getCookieFromFile()
        self.assertEqual(cookies['domain'], 'datawarehouse.dbd.go.th')
        self.assertEqual(cookies['httpOnly'], True)
        self.assertEqual(cookies['name'], 'JSESSIONID')
        self.assertEqual(cookies['path'], '/')
        self.assertEqual(cookies['secure'], False)
        self.assertEqual(cookies['value'], 'ZDYxOWM4MzEtMjIwMS00YTA4LWE4YmUtY2Y1N2VmOTdiMzZk')

    def test_getPage(self):
        url = 'file:///dbdv2/tests/test_data/hello.html'
        page = self.browser.getPage(url)
        self.assertEqual(page[1],'hello')

    def test_getCookieFromWeb(self):
        result = self.browser.getCookieFromWeb()
        self.assertNotEqual(result, '')
        self.assertEqual(result['name'], 'JSESSIONID')

    '''
    def test_checkCookie(self):
        url = 'file:///dbdv2/test/test_data/cookie.html'

        cookie = {'name':'username', 'value':'asdf','path' : '/'}
        try:
            result = self.browser.checkCookie(cookie, url)
        except exceptions.InvalidCookieDomainException as e:
            print(e)
        #self.assertEqual(result, True)

        cookie['value'] = 'qwer'
        try:
            result = self.browser.checkCookie(cookie, url)
        except exceptions.InvalidCookieDomainException as e:
            print(e)
        #self.assertEqual(result, False)
    '''
        

    
        



if __name__ == "__main__":
    unittest.main()
