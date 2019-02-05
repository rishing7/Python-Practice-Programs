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


class Developer(Employee):
    raise_amount = 1.10

    def __init__(self, fname, lname, pay, prog_lang):
        super().__init__(fname, lname, pay)
        self.prog_lang = prog_lang



class Manager(Employee):
    def __init__(self, fname, lname, pay, employees = None):
        super().__init__(fname, lname, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees
    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emps(self):
        for emp in self.employees:
            print('-->' + emp.fullName())


dev1 = Developer('rishikesh', 'rishi', 1000, "python")
dev1.apply_raise()
print(dev1.apply_raise())
dev2 = Developer('aaa', 'bbb', 110000, "python")
emp1 = Employee('xyz', 'abc', 1000)
print(emp1.apply_raise())
emp2 = Employee('abc', 'xyz', 500)
print(dev1.email)

manager1 = Manager('nnn', 'aaa', 1234500, [dev1, dev2, emp1, emp2])
print(manager1.print_emps())

print(isinstance(manager1, Manager))