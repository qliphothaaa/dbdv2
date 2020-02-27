import unittest
from browser.scraping_browser import ScrapingBrowser
from selenium.common import exceptions

class TestScrapingBrowser(unittest.TestCase):
    def setUp(self):
        self.browser = ScrapingBrowser()

    def tearDown(self):
        self.browser.close()


    def test_getPage(self):
        url = 'file:///dbdv2/tests/test_data/hello.html'
        page = self.browser.getPage(url)
        self.assertEqual(page[1],'hello')
        self.assertEqual(page[2],'200')

        url = 'file:///dbdv2/tests/test_data/Error.html'
        page = self.browser.getPage(url)
        self.assertEqual(page[1],'Error | DBD')
        self.assertEqual(page[2],'401')


if __name__ == "__main__":
    unittest.main()
