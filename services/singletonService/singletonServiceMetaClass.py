# !/usr/bin/python3


class SingletonMetaClass(type):
    """
    Example :
    class SingletonMetaClass(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    class AAA(metaclass=SingletonMetaClass):
        def __init__(self,val):
            self.val = val
        def __str__(self):
            return self.val
    x=AAA('sausage')
    y=AAA('eggs')
    z=AAA('spam')
    print(x)
    print(y)
    print(z)
    print(x is y is z)
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @staticmethod
    def clear():
        SingletonMetaClass._instances = {}
