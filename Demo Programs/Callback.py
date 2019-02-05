myList = ['rishi', 'atul', 'raj']
def addElement(name, callback):
    myList.append(name)

def getList():
    print(myList)


addElement('kumar', getList)