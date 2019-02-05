t = int(input())
for i in range(t):
    n = int(input())
    arr = [int(x) for x in input().split()]
    arr.sort(reverse = True)
    # print(arr)
    sum = 0
    for l in range(0, len(arr), 4):
        sum+=arr[l]
        if(len(arr)>=2):
            sum += arr[l+1]
    print(sum)