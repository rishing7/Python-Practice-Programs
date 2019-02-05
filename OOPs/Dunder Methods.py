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

    def __repr__(self):
        return "Employee({}, {}, {})".format(self.fname, self.lname, self.pay)

    def __str__(self):
        return "{} -> {}".format(self.fullName(), self.email)


emp_1 = Employee('rrr', 'kkk', 320000)
print(repr(emp_1))
print(str(emp_1))