def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mul(a,b):
    return a*b
def divide(a,b):
    if b==0:
        raise ValueError('Can not be divided by 0')
    return a/b


print(add(9,7))