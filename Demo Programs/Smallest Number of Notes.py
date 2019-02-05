t = int(input())
for i in range(t):
    n = int(input())
    # arr = [int(x) for x in input().split()]
    count = 0
    if n%100 == 0:
        count = int(n/100)
        n = n % 100
    elif n%100 != 0:
        count += int(n/100)
        n = n % 100
    if n%50 == 0:
        count += int(n/50)
        n = n % 50
    elif n%50 != 0:
        count += int(n/50)
        n = n % 50
    if n%10 == 0:
        count += int(n/10)
        n = n % 10
    elif n%10 != 0:
        count += int(n/10)
        n = n % 10
    if n%5 == 0:
        count += int(n/5)
        n = n % 5
    elif n%5 != 0:
        count += int(n/5)
        n = n % 5
    if n%2 == 0:
        count += int(n/2)
        n = n % 2
    elif n%2 != 0:
        count += int(n/2)
        n = n % 2
    if n%1 == 0 and n==1:
        count += int(n/1)
        n = n % 1
    print(count)


