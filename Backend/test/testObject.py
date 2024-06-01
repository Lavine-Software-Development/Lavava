from Backend.test.old_method_mulitplier import method_multipliers


def multiplier():
    return 3

def comp_multiplier(bean):
    return bean

@method_multipliers({('default', multiplier), ('param', comp_multiplier)})
class TestObject:

    def default(self):
        return 2
    
    def param(self, bean):
        return bean
    
    def print(self, bean=None):
        if bean:
            print(self.param(bean))
        else:
            print(self.default())
    

tob = TestObject()
tob2 = TestObject()
tob.print()
tob.print(5)
tob.apply_modifications()
tob3 = TestObject()
tob.print()
tob.print(5)
tob2.print()
tob2.print(5)
tob3.print()
tob3.print(5)
    