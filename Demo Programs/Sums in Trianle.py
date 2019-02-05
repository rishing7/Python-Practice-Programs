t = int(input())
for i in range(t):
    n = int(input())
    matrix = [[int(x) for x in input().split()] for y in range(n)]
    # print(matrix)
    res = 0
    for i in range(n-1, 0, -1):
        res = res + max(matrix[i])
    print(res)