try:
    a = 10 / 2
    # print('rishi' + 10)

except TypeError as te:
    print(te)

except ArithmeticError:
    print("Unknown error occurred")

else:
    print('No Exceptions')

finally:
    print("finally")