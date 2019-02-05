"""
    Class variable is shared among each instance.
"""


class Employee:
    no_of_emps = 0
    raise_amount = 1.05   # 5% increment

    def __init__(self, fname, lname, pay):
        self.fname = fname
        self.lname = lname
        self.pay = pay
        self.email = fname + '.' + lname + '@company.com'
        Employee.no_of_emps += 1        # I am not using self.no_of_emps reason is that i have to count.

    def fullName(self):
        return '{} {}'.format(self.fname, self.lname)

    def apply_raise(self):
        return int(self.pay*self.raise_amount)      # Employee.raise_amount can be used but instance can't change it.


print(Employee.no_of_emps)
emp_1 = Employee('rishikesh', 'rishi', 90000)
print(emp_1.email)
print(emp_1.__dict__)

emp_1.raise_amount = 1.10
print(emp_1.__dict__)
print(Employee.__dict__)
Employee.raise_amount = 1.20
print(Employee.__dict__)

emp_2 = Employee('aaa', 'bbb', 110000)
print(Employee.fullName(emp_2))

print(Employee.no_of_emps)