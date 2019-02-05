""" This module converts an id to base 62([a-zA-Z0-9) format string."""


def idToShortURL(_id):
    shortURL = []
    possibleElements = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    while _id != 0:
        shortURL.append(possibleElements[_id % 62])
        _id = _id // 62

    if _id == 0:
        shortURL.append(possibleElements[_id % 62])
    shortURL.reverse()
    return ''.join(shortURL)


if __name__ == '__main__':
    print(idToShortURL(620))