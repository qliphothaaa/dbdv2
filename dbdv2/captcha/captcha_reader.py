import pytesseract
from PIL import Image

def readCaptcha(img):
    result = ''

    try:
        screen = Image.open(img)
    except:
        print('no Image')
        return ''
    #screen = screen[1120:1200, 375:638]
    #370/1600, 1120/1200, 643/1600, 1200/1200
    #370/size[0], 1120/size[1], 643/size[0], size[1]
    width, height = screen.size
    captcha = screen.crop((370/1600*width, 1120/1200*height, 600/1600*width, height))
    captcha = captcha.convert('RGB')
    #captcha.show()
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

    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        img = sys.argv[1]
    #img= 'screenshot.png'
    print(readCaptcha(img))
    
