import logging as log
import os
import hashlib
import PIL.Image as Img

log.basicConfig(level=log.INFO)

def compare_by_hash(path_to_original: str, path_to_copy: str) -> tuple[bool, str, str]:
    """
    Compares two files by its hashes.
    """
    orig_hash = hashlib.sha256()
    copy_hash = hashlib.sha256()

    with open(path_to_original, 'rb') as img:
        orig_hash.update(img.read())
    log.debug(('Hash (SHA256) of ' + os.path.basename(path_to_original) + ' is: ').ljust(50) + orig_hash.hexdigest())

    with open(path_to_copy, 'rb') as img:
        copy_hash.update(img.read())
    log.debug(('Hash (SHA256) of ' + os.path.basename(path_to_copy) + ' is: ').ljust(50) + copy_hash.hexdigest())

    return orig_hash.hexdigest() == copy_hash.hexdigest(), orig_hash.hexdigest(), copy_hash.hexdigest()


def get_file_info(path: str) -> dict:
    """
    Gets basic info about file as dictionary.
    """
    try:
        img = Img.open(path)

        info = {
            'name': os.path.basename(path),
            'width': img.width,
            'height': img.height,
            'size': os.stat(path).st_size,
            'channels': img.mode,
            'format': img.format,
        }

        dpi = img.info.get('dpi')
        info['dpi'] = round(dpi[0]) if dpi else '-'

        img.close()
        return info
    except Exception as e:
        log.error('File ' + path + ' is not an image or file not found!- Reason: ' + str(e))


def compare_by_pixels(path_to_original: str, path_to_copy: str) -> list[dict]:
    """
    Compares two images pixel by pixel and returns list of dictionaries of different pixels.
    """
    try:
        orig_img = Img.open(path_to_original)
        copy_img = Img.open(path_to_copy)

        if orig_img.size != copy_img.size:
            log.warning('Images have different resolutions - Cannot compare them!')
            return 'Images have different resolutions - Cannot compare them!'
        
        diff_pixels = []
        print('\nPIXEL DIFFERENCE BETWEEN IMAGES:')
        print('Position'.ljust(30) + os.path.basename(path_to_original).ljust(30) + os.path.basename(path_to_copy))
        for x in range(orig_img.width):
            for y in range(orig_img.height):
                orig_pixel = orig_img.getpixel((x, y))
                copy_pixel = copy_img.getpixel((x, y))
                if orig_pixel != copy_pixel:
                    diff_pixels.append({'position': (x, y), 'original_pixel': orig_pixel, 'copy_pixel': copy_pixel})
                    print(('x: ' + str(x) + '; y: ' + str(y)).ljust(30) + str(orig_pixel).ljust(30) + str(copy_pixel))
        print('No different pixels between images!\n') if diff_pixels == [] else print()
        orig_img.close()
        copy_img.close()
        return diff_pixels

    except:
        log.error('Error accrued during processing!')
        return 'Error accrued during processing!'
