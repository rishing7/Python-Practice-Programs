string = "ABCDCDC"
sub_string = "CDC"
l = list(string)
s = list(sub_string)
print("S1:{}\nS2:{}".format(l,s))
i=0
count=0
try:
    while (i < len(l)):
        if (l[i] == s[i]):
            j = i
            flag = 0
            while (l[j] == s[j]):
                flag += 1
                j += 1
            if (flag == len(s)):
                count += 1
        i += 1
except IndexError:
    print("Found")
    print(count)