# Method 1


def leftRotate1(arr, d, n):
    for i in range(0, d):
        temp = arr[0]
        for j in range(len(arr) - 1):
            arr[j] = arr[j + 1]
        arr[len(arr) - 1] = temp


# Method 2


def leftRotate2(arr, d, n):
    myList = []
    for i in range(d):
        myList.append(arr[i])
    k = 0
    for i in range(d, n):
        arr[k] = arr[i]
        k += 1
    print(myList)
    p = 0
    for i in range(n - d, n):
        arr[i] = myList[p]
        p += 1
    print(myList)


# Method 3


arr = [1, 2, 3, 4, 5]
print(arr)
leftRotate2(arr, 2, len(arr))
print(arr)
