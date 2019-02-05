"""
    Here we are creating instance variables those are unique to each employee.
    There are two ways to call a method.
"""


class Employee:
    def __init__(self, fname, lname, pay):
        self.fname = fname
        self.lname = lname
        self.pay = pay
        self.email = fname + '.' + lname + '@company.com'

    def fullName(self):
        return '{} {}'.format(self.fname, self.lname)


emp_1 = Employee('rishikesh', 'rishi', 90000)
print(emp_1.email)

emp_2 = Employee('aaa', 'bbb', 110000)
print(Employee.fullName(emp_2))


########################## GETATTR #########################

var = emp_1.fullName