t = int(input())
for i in range(t):
    a,b = input().split()
    a = int(a)
    b = int(b)
    res = 0
    if a>b:
        print(a, end=' ')
    else:
        print(b, end=' ')
    print(a+b)