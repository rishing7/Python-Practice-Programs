"""
    Regular Methods, Class Methods and Static Methods
    1. Regular method takes by default one variable/instance in my convention it is self
    2. Class method doesn't use self instance by default it uses decorator @classmethod
"""


class Employee:
    no_of_emps = 0
    raise_amount = 1.05  # 5% increment

    def __init__(self, fname, lname, pay):
        self.fname = fname
        self.lname = lname
        self.pay = pay
        self.email = fname + '.' + lname + '@company.com'
        Employee.no_of_emps += 1  # I am not using self.no_of_emps reason is that i have to count.

    def fullName(self):
        return '{} {}'.format(self.fname, self.lname)

    def apply_raise(self):
        return int(self.pay * self.raise_amount)  # Employee.raise_amount can be used but instance can't change it.

    @classmethod
    def set_raise_amount(cls, amount):  # No self instance
        cls.raise_amount = amount

    @classmethod
    def from_string(cls, emp_str):
        fname, lname, pay = emp_str.split('-')
        return cls(fname, lname, pay)


Employee.set_raise_amount(1.25)
print(Employee.raise_amount)

emp1_string = "rishikesh-kumar-110000"

emp1 = Employee.from_string(emp1_string)
print(emp1.email)