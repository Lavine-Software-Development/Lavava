
def inheritance_decorator(*args):
    def decorator(cls):
        cls.tracked_attrs = list(args) + getattr(cls, 'tracked_attrs' , [])
        for arg in cls.tracked_attrs:
            setattr(cls, arg, None)
        return cls
    return decorator

@inheritance_decorator('parent')
class Parent:
    pass

@inheritance_decorator('child')
class Child(Parent):
    
    def __init__(self):
        self.bean = "beani"
        print(Child.__dict__)


child = Child()
child2 = Child()
child.child = 5
child2.child = 6
child.parent = 2
child2.parent = 3
print(child.__dict__)
print(child2.__dict__)
