import unittest
from browser.captcha_reader import readCaptcha


class TestCaptchaReader(unittest.TestCase):

    def test_readCaptcha(self):
        img_path=['tests/test_data/screenshot1.png','tests/test_data/screenshot2.png','tests/test_data/screenshot3.png']
        #for i in img_path:
            #print(readCaptcha(i))
        self.assertEqual(readCaptcha(img_path[0]),'yp8xd')
        self.assertEqual(readCaptcha(img_path[1]),'abpxp')
        self.assertEqual(readCaptcha(img_path[2]),'agxrd')
        

if __name__ == "__main__":
    unittest.main()
