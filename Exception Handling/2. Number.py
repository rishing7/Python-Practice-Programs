"""
    When there is no exception in try block then else block gets executed otherwise except block gets executed.
    If try block has exception but in except block it doesn't match with the mentioned exception then abnormal
    termination takes place without executing the else block code.
"""

try:
    a = 6
    if a < 4:
        b = a/(a-3)
        print('Value of b is: ', b)

except(ZeroDivisionError, NameError):
    print("An error occurred!")

else:
    print('Welcome!!!')