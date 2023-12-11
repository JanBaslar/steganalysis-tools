import logging as log
from PIL import Image as Img


def hide_message_into_image(path: str, message: str, channel: int, offset: int) -> None:
    """Hides message into image using most primitive LSB method."""
    try:
        img = Img.open(path)
        binary = ''.join([bin(ord(letter))[2:].zfill(8) for letter in message])
        index = 0
        end = False
        for x in range(img.width):
            for y in range(img.height):
                if (x * img.width + y) >= offset:
                    pix_value = img.getpixel((x, y))
                    if pix_value[channel] % 2 != int(binary[index]):
                        new_value = list(pix_value)
                        new_value[channel] += 1
                        img.putpixel((x, y), tuple(new_value))
                    index += 1
                    if index == len(binary):
                        end = True
                        break
            if end:
                break

        img.save('C:/Users/jbaslar/Pictures/Demo/picture.png')
        img.close()
        log.info('Message was hidden successfully.')
    except Exception as e:
        log.error('Error accrued during processing: ' + str(e))
        return 'Error accrued during processing!'
    
hide_message_into_image('C:/Users/jbaslar/Pictures/Demo/original.png', '\nThese are some secret data hidden by LSB method.\n', 2, 64)
