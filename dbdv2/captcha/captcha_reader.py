import pytesseract
from PIL import Image

def readCaptcha(img):
    result = ''
    captcha = Image.open(img)
    if captcha is not None:
        #captcha = captcha[1120:1200, 375:638]
        captcha = captcha.crop((370, 1120, 643, 1200))
        captcha = captcha.convert('RGB')
        color = captcha.getpixel((2,2))
        #color = np.array([point[0],point[1],point[2]])
        #height, width, _ = captcha.shape
        width, height = captcha.size
        pixels = captcha.load()
        '''
        for h in range(0,height):
            for w in range(0,width):
                if (captcha[h,w] == color).all():
                    captcha[h,w] = (255,255,255)
                else:
                    captcha[h,w] = (0,0,0)
        '''
        for i in range(width):
            for j in range(height):
                if pixels[i, j] != color:
                    pixels[i, j] = (0,0,0)
                else:
                    pixels[i, j] = (255,255,255)

        result = pytesseract.image_to_string(captcha, lang='eng', config='--dpi 100 --psm 7')
    else:
        print('No Image!')

    return result


if __name__ == "__main__":
    img= 'screenshot.png'
    print(readCaptcha(img))
    
