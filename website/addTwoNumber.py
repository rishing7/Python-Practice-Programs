
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

head=None
def generateLinkList(sum):
    global  head
    if (head == None):
        head = ListNode(sum)
    else:
        current = head
        while (current.next != None):
            current = current.next
        current.next = ListNode(sum)
    return head



class Solution(object):
    def addTwoNumbers(self, l1, l2):
        stack1=Stack()
        stack2=Stack()
        while l1!=None:
            stack1.push(l1.val)
            l1=l1.next
        while l2!=None:
            stack2.push(l2.val)
            l2=l2.next

        # while stack1.isEmpty()!=True :
        #     print(stack1.pop(),)
        # while stack2.isEmpty()!=True :
        #     print("yahi hota pyar ",stack2.pop())
        carry,sum,temp=0,0,0
        while stack1.isEmpty() is not True and stack2.isEmpty() is not True:
            sum=stack1.pop()+stack2.pop()+carry
            if sum>10:
                temp=sum
                sum=sum%10
                carry=temp//10
            else:
                carry=0
            print ("sum,carry all",sum,carry)
            generateLinkList(sum)
        while stack1.isEmpty() is not True:
            sum = stack1.pop() + carry
            if sum > 10:
                temp = sum
                sum = sum % 10
                carry = temp // 10
            else:
                carry=0
            print("sum,carry stack1", sum, carry)
            generateLinkList(sum)
        while stack2.isEmpty() is not True:
            sum = stack2.pop() + carry
            if sum > 10:
                temp = sum
                sum = sum % 10
                carry = temp // 10
            else:
                carry=0
            print("sum,carry stack2", sum, carry)
            generateLinkList(sum)
        if carry>0:
            generateLinkList(carry)
        return  head
if __name__=="__main__":
    s=Solution()
    head1=ListNode(2)
    first=ListNode(3)
    second=ListNode(9)
    head1.next=first
    first.next=second
    head2=None
    # head2 = ListNode(5)
    # first1 = ListNode(3)
    # head2.next = first1


    print (s.addTwoNumbers(head1,head2))
    while(head!=None):
        print (head.val)
        head=head.next


