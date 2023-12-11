import logging as log
import PIL.Image as Img

def get_img_histogram(path: str) -> list[int]:
    """Gets histogram of image"""
    try:
        img = Img.open(path)
        rgba = img.split()
        img.close()
        return rgba[0].histogram(), rgba[1].histogram(), rgba[2].histogram()
    except Exception as e:
        log.error(e)


def detect_strings(path: str, channel: int, offset: int) -> list[str]:
    """Detect strings hidden in images."""
    try:
        img = Img.open(path)
        
        strings = ''
        binary = ''
        log.debug('\nDETECTED STRINGS INSIDE IMAGE:')
        for x in range(img.width):
            for y in range(img.height):
                if (x * img.width + y) >= offset:
                    pixel = img.getpixel((x, y))
                    binary += str(pixel[channel] % 2)
                    if len(binary) == 8:
                        strings += chr(int(binary, 2))
                        binary = ''
                    
        log.debug(strings)
        img.close()
        return strings

    except:
        log.error('Error accrued during processing!')
        return 'Error accrued during processing!'
    
def detect_odd_pixels(path: str) -> list[dict]:
    """Detects odd pixels in images."""
    try:
        img = Img.open(path)
        
        odd_pixels = []
        print('\nDETECTED ODD PIXELS INSIDE IMAGE:')
        print('Position'.ljust(30) + 'Pixel value'.ljust(30) + 'Expected pixel value')
        for x in range(2, img.width - 3):
            for y in range(2, img.height - 3):

                surrounding_pixels = []
                for i in range(x-2, x+3):
                    for j in range(y-2, y+3):
                        surrounding_pixels.append(img.getpixel((i, j)))

                suspicious_pixel = surrounding_pixels.pop(12)
                surrounding_set = set(surrounding_pixels)
                expected_pixel = list(surrounding_set)[0]
                if len(surrounding_set) == 1 and expected_pixel != suspicious_pixel:
                    odd_pixels.append({'position': (x, y), 'pixel': suspicious_pixel, 'expected': expected_pixel})
                    print(('x: ' + str(x) + '; y: ' + str(y)).ljust(30) + str(suspicious_pixel).ljust(30) + str(expected_pixel))
        
        if odd_pixels == []: print('No odd pixels detected in image.')
        img.close()
        return odd_pixels

    except Exception as e:
        log.error('Error accrued during processing! ' + str(e))
        return 'Error accrued during processing!'
    
    