import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


def goToRegistry(imei, jToken):
    uname = 'rishi'
    psw = 'rishi'
    cluster_id = 'tyui'
    myData = []
    myData.append(uname)
    myData.append(psw)
    myData.append(cluster_id)

    # a list
    # hits the mqtt broker
    # subscibe at a particular topic
    # get the cluster_id, Uname and password

    return myData
def getJtoken(imei):
    # imei number is checked
    jToken = randomword(20)
    print(jToken)
    return goToRegistry(imei, jToken)



print(getJtoken("oiuytdcvbjopoiugfvcbkl"))