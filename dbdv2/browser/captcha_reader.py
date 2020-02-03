import pytesseract
from PIL import Image

def readCaptcha(img_path):
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


if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        img = sys.argv[1]
    #img= 'screenshot.png'
    print(readCaptcha(img))
    
