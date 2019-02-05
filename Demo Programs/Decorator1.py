def bold(func):
    def wrapper(*args):
        return "<b>" + func(*args) + "</b>"
    return wrapper


def italic(func):
    def wrapper(*args):
        return "<i>" + func(*args) + "</i>"
    return wrapper


@italic
@bold
def formattedText():
    return 'rishi'


print(formattedText())
