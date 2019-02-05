"""
    Here i am using is_work_day method is work day or not because this is not dependable on any instance
"""

import datetime




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

    @staticmethod
    def is_work_day(day):
        if day.weekday() is 5 or day.weekday() is 6:
            return False
        else:
            return True

emp1_string = "rishikesh-kumar-110000"

emp1 = Employee.from_string(emp1_string)
print(emp1.email)

mydate = datetime.date(2018, 12, 24)
print(Employee.is_work_day(mydate))
