import inspect
from functools import wraps

def method_multipliers(modifications):
    def class_decorator(cls):
        cls._method_modifications = modifications

        @classmethod
        def apply_modifications(cls):
            for original_name, modifier_function in cls._method_modifications:
                original_method = getattr(cls, original_name)
                create_modified_method(cls, original_name, original_method, modifier_function)

        def create_modified_method(cls, original_name, original_method, modifier_function):
            modifier_sig = inspect.signature(modifier_function)
            original_sig = inspect.signature(original_method)

            include_self = 'self' in modifier_sig.parameters
            required_names = set(modifier_sig.parameters.keys()) - {'self'}
            index_map = [i for i, (name, param) in enumerate(original_sig.parameters.items()) if name in required_names]

            if include_self:
                @wraps(original_method)
                def modified_method_with_self(self, *args):
                    mod_args = (self,) + tuple(args[i - 1] for i in index_map)
                    return original_method(self, *args) * modifier_function(*mod_args)
                setattr(cls, original_name, modified_method_with_self)
            else:
                @wraps(original_method)
                def modified_method_without_self(self, *args):
                    mod_args = tuple(args[i - 1] for i in index_map)
                    return original_method(self, *args) * modifier_function(*mod_args)
                setattr(cls, original_name, modified_method_without_self)

        cls.apply_modifications = apply_modifications
        return cls
    return class_decorator
