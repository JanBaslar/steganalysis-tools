def calculate_img_size(width: int, height: int, max_allowed_width=230, max_allowed_height=180) -> tuple[int, int]:
    """Calculates width and height of image to fit it into preview label"""
    new_height = round(height / width * max_allowed_width)
    if new_height <= max_allowed_height:
        return max_allowed_width, new_height
    new_width = round(width / height * max_allowed_height)
    return new_width, max_allowed_height


def dict_to_info(info_dict: dict) -> str:
    """Reformats dictionary to file info string"""
    result = info_dict.get('name') + '\n'
    result += 'Resolution: ' + str(info_dict.get('width')) + 'x' + str(info_dict.get('height')) + '\n'
    result += 'Size: ' + to_readable(info_dict.get('size')) + '\n'
    result += 'Channels: ' + str(info_dict.get('channels')) + '\n'
    result += 'DPI: ' + str(info_dict.get('dpi')) + '\n'
    result += 'Format: ' + str(info_dict.get('format'))
    return result


def to_readable(bytes: int) -> str:
    """Changes size in bytes to more human readable form"""
    units = [' B', ' kB', ' MB', ' GB', ' TB']
    index = 0
    while bytes > 1024:
        bytes = bytes / 1024
        index += 1
    return str(round(bytes, 2)) + units[index]
