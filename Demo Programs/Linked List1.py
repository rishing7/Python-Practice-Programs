class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def addAtEnd(self, data):
        temp = self.head
        while(temp.next):
            temp = temp.next
        temp.next = Node(data)

    def addAtStarting(self, data):
        temp = self.head
        if not temp:
            temp.next = Node(data)
        else:
            newNode = Node(data)
            newNode.next = self.head
            self.head = newNode
    def addAtPosition(self, data, position):
        temp = self.head
        newNode = Node(data)
        count = 0
        while(temp):
            temp = temp.next
            count += 1
            if(count == position):
                break
            temp1 = temp.next
            temp.next = newNode
            newNode.next = temp1
        print(count)

    def reverseList(self):
        temp = self.head
        prevNode = None
        nextNode = None
        while(temp):
            nextNode = temp.next
            temp.next = prevNode
            prevNode = temp
            temp = nextNode
        self.head = prevNode
    def printLinkedList(self):
            temp = self.head
            while(temp):
                print(temp.data, end=' ')
                temp = temp.next
            print()

if __name__ == '__main__':
    llist = LinkedList()
    first = Node(1)
    second = Node(2)
    third = Node(3)
    llist.head = first
    first.next = second
    second.next = third
    third.next = None
    llist.printLinkedList()
    llist.addAtEnd(10)
    llist.printLinkedList()
    llist.addAtStarting(0)
    llist.printLinkedList()
    llist.addAtPosition(4,1)
    llist.printLinkedList()
    print('Reversing of linked list')
    llist.reverseList()
    llist.printLinkedList()