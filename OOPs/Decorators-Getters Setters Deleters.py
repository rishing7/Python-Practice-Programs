class Employee:
    raise_amount = 1.05  # 5% increment

    def __init__(self, fname, lname, pay):
        self.fname = fname
        self.lname = lname
        self.pay = pay
        # self.email = fname + '.' + lname + '@company.com'

    @property    # emp.email can be called directly instead email()
    def email(self):
        return '{}.{}@email.com'.format(self.fname, self.lname)

    @property
    def fullName(self):
        return '{} {}'.format(self.fname, self.lname)

    @fullName.setter            # To use the line No-32 statement
    def fullName(self, name):
        fname, lname = name.split(' ')
        self.fname = fname
        self.lname = lname

    @fullName.deleter
    def fullName(self):
        print('Delete Name!')
        self.fname = None
        self.lname = None


emp_1 = Employee('aaa', 'bbb', 100000)

print(emp_1.fname)
print(emp_1.email)
print(emp_1.fullName)


emp_1.fullName = 'rishikesh Kumar'


print(emp_1.fname)
print(emp_1.email)
print(emp_1.fullName)

del emp_1.fullName

print(emp_1.fname)
print(emp_1.email)
print(emp_1.fullName)