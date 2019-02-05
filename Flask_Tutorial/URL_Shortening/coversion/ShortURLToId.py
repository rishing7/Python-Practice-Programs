""" This module converts a string into base 10 format(decimal) id."""


def shortURLTo_id(shortURL):
    _id = 0
    for i, _ in enumerate(shortURL):
        if 'a' <= shortURL[i] <= 'z':
            _id = _id * 62 + ord(shortURL[i])-ord('a')
        if 'A' <= shortURL[i] <= 'Z':
            _id = _id * 62 + ord(shortURL[i])-ord('A') + 26
        if '0' <= shortURL[i] <= '9':
            _id = _id * 62 + ord(shortURL[i]) - ord('9') + 52
    return _id


if __name__ == '__main__':
    print(shortURLTo_id('aka'))