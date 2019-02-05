arr = [2,4,6]
for i in range(0,8):
    l = list('{:0b}'.format(i))
    print(l)
    for j in range(0, len(l)):
            if (l[j] == '1'):
                print(arr[j], sep=' ', end=' ')
    print(',')