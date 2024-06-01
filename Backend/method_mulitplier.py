import inspect
from functools import wraps

def method_multipliers(modifications):
    def class_decorator(cls):
        cls._method_modifications = modifications

        def apply_modifications(self):
            for original_name, modifier_function in self._method_modifications:
                original_method = getattr(self, original_name)
                self.create_modified_method(original_name, original_method, modifier_function)

        def create_modified_method(self, original_name, original_method, modifier_function):
            modifier_sig = inspect.signature(modifier_function)
            original_sig = inspect.signature(original_method)

            include_self = 'self' in modifier_sig.parameters
            required_names = set(modifier_sig.parameters.keys()) - {'self'}
            index_map = [i for i, (name, param) in enumerate(original_sig.parameters.items()) if name in required_names]

            if include_self:
                @wraps(original_method)
                def modified_method_with_self(*args):
                    mod_args = (self,) + tuple(args[i] for i in index_map)
                    return original_method(*args) * modifier_function(*mod_args)
                setattr(self, original_name, modified_method_with_self)
            else:
                @wraps(original_method)
                def modified_method_without_self(*args):
                    mod_args = tuple(args[i] for i in index_map)
                    return original_method(*args) * modifier_function(*mod_args)
                setattr(self, original_name, modified_method_without_self)

        setattr(cls, 'apply_modifications', apply_modifications)
        setattr(cls, 'create_modified_method', create_modified_method)
        return cls
    return class_decorator
