import os
from random import randint
import logging as log
from PIL import Image as Img

def reformat_image(old_path: str, new_path: str, format: str) -> None:
    """Loads image from old path and saves it to new path."""
    with Img.open(old_path) as img:
        if format == 'JPG':
            img = img.convert('RGB')
        img.save(new_path)


def compress_image(old_path: str, new_path: str, quality: int) -> None:
    """Compress image from old path to new path."""
    with Img.open(old_path) as img:
        if os.path.splitext(new_path)[1] == '.png':
            w, h = img.size
            ratio = quality / 100
            img = img.resize((round(w * ratio), round(h * ratio)))
        img.save(new_path, optimize=True, quality=quality)


def enhance_image(old_path: str, new_path: str, channel: int, percent: int) -> None:
    """Enhance image by random bits"""
    try:
        img = Img.open(old_path)
        enhanced_pixels = 0
        print('\nEnhancing began')
        for x in range(0, img.width):
            for y in range(0, img.height):
                if randint(0, 100) < percent:
                    pixel = img.getpixel((x, y))
                    new_pixel = list(pixel)
                    if new_pixel[channel] > 0: 
                        new_pixel[channel] -= 1 
                    else: 
                        new_pixel[channel] += 1
                    img.putpixel((x, y), tuple(new_pixel))
                    enhanced_pixels += 1
        print(str(enhanced_pixels) + ' pixels were changed (' + str(round(enhanced_pixels / (img.width * img.height) * 100, 2)) + ' %)')
        img.save(new_path)
        img.close()
        print('Enhancing ended')

    except Exception as e:
        log.error('Error accrued during processing! ' + str(e))
        return 'Error accrued during processing!'