class Abc:
    """
    This is a demo class
    """

    def __init__(self, x, y):
        """
        This is a constructor to instantiate the object.
        :param x:
        :param y:
        """
        self.x = x
        self.y = y

    def sum(self):
        """
        It sums two integers.
        :return: and return summation of them.
        """
        return self.x + self.y


obj = Abc(10, 13)

'''hasattr(object, ' name of the attribute ') : It returns the binary output whether specified attribute is there or 
not '''
print(hasattr(obj, 'x'))
print(hasattr(obj, 'sum'))
print(hasattr(obj, 'z'))

'''getattr(object, name of the attribute that needed) : It returns the value of that attribute'''
print(getattr(obj, 'x'))
print(getattr(obj, 'sum')())
'''Gives an error'''
# print(getattr(obj, 'z'))
print(getattr(obj, 'z', 1000))  # Returns default value
''' Still gives an error '''
# print(getattr(obj, 'z'))

'''setattr(object, to be set or overridden )'''

print(setattr(obj, 'z', 100))
print(hasattr(obj, 'z'))
print(getattr(obj, 'z'))

''' Overriding '''
print(setattr(obj, 'x', 100))
print(getattr(obj, 'x'))
