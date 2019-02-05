import time


def decorator_fun(func):
    def wrapper_func(*args, **kwargs):
        start = time.time()
        print(start)
        res = func(*args, **kwargs)
        end = time.time()
        print(end)
        print(func.__name__ + " took "+ str((end-start)*1000) + " mil sec")
        return res
    return wrapper_func


@decorator_fun
def square(a):
    time.sleep(0.1)
    print(a*a)


@decorator_fun
def cube(a):
    print(a*a*a)

square(10)
cube(100)