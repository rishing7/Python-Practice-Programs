t = int(input())
for i in range(t):
    n = int(input())
    res = 0
    for i in range(11, -1, -1):
        res = res + int(n/pow(2, i))
        n = n%pow(2, i)
    print(res)
