t = int(input())
for i in range(t):
    a, b, c = input().split()
    a = int(a)
    b = int(b)
    c = int(c)
    if a>b and a<c or a<b and a>c:
        res = a
    elif b>a and b<c or b<a and b>c:
        res = b
    elif c>a and c<a or c<a and c>a:
        res = c
    elif a==b and a>c:
        res = c
    elif a==b and c>a:
        res = a
    elif b==c and b>a:
        res = a
    elif b==c and b<c:
        res = b
    elif c==a and c>b:
        res = b
    elif c==a and c<b:
        res = c
    print(res)