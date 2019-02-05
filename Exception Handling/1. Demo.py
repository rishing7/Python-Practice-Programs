inputList = [1, 7, 8, 9]
print(inputList)

try:
    print("3rd element in the list is: ", inputList[2])
    print("5th element in the list is: ", inputList[4])
except IndexError:
    print("Index is not reachable:)\nCheckout try part of the code")
