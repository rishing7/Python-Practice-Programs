
def main():
    arr = [0,0,-1,9]
    s = len(arr)
    res = 0
    sum = 0
    l=0
    h=0
    for i in range(0,s):
        if arr[i]>=0:
            sum+=arr[i]
        elif arr[i]<0:
            if sum>=res:
                res = sum
                sum = 0
                l = l
                h = i
            i +=1
    #print(res)
    for i in range(l, h):
        print(arr[i])
if __name__ == '__main__':main()
