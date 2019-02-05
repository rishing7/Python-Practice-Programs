n, R = map(int, input().split())
l = []
for i in range(n):
    l.append(int(input()))
for i in l:
    if i >= R:
        print("Good boi")
    else:
        print("Bad boi")
