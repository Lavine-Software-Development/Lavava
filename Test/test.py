from simple_tcd_w import watch_attributes
import pytest

class ReferenceClass:
    def __init__(self):
        self.var = 0

@watch_attributes("base_variable", "reference")
class BaseClass:
    def __init__(self, reference: ReferenceClass):
        self.base_variable = 0
        self.reference = reference
        self.untracked = "hello"

@watch_attributes("child_variable")
class ChildClass(BaseClass):
    def __init__(self, reference: ReferenceClass):
        super().__init__(reference)
        self.child_variable = 0
        self.bean = "beani"


# def test_base_class():
#     ref = ReferenceClass()
#     base = BaseClass(ref)

#     base.base_variable = 5
#     base.reference.var = 5
#     assert base.updated == {"base_variable"}

#     base.clear()
#     base.reference = ReferenceClass()
#     base.untracked = "hi"
#     base.base_variable = 5
#     assert base.updated == {"reference"}


def test_child_class():
    ref = ReferenceClass()
    child = ChildClass(ref)

    child.base_variable = 5
    child.child_variable = 5
    assert child.updated == {"base_variable", "child_variable"}

    child.clear()
    assert child.updated == set()

    print(child.__dict__)
    print(child._original.__dict__)
    print(child._original._original.__dict__)