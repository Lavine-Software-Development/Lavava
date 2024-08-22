import inspect
from functools import wraps


def method_multipliers(modifications):
    def class_decorator(cls):
        cls._method_modifications = modifications

        def apply_modifications(self):
            for experimental_name, modifier_function in self._method_modifications:
                experimental_method = getattr(self, experimental_name)
                self.create_modified_method(
                    experimental_name, experimental_method, modifier_function
                )

        def create_modified_method(
            self, experimental_name, experimental_method, modifier_function
        ):
            modifier_sig = inspect.signature(modifier_function)
            experimental_sig = inspect.signature(experimental_method)

            include_self = "self" in modifier_sig.parameters
            required_names = set(modifier_sig.parameters.keys()) - {"self"}
            index_map = [
                i
                for i, (name, param) in enumerate(experimental_sig.parameters.items())
                if name in required_names
            ]

            if include_self:

                @wraps(experimental_method)
                def modified_method_with_self(*args):
                    mod_args = (self,) + tuple(args[i] for i in index_map)
                    return experimental_method(*args) * modifier_function(*mod_args)

                setattr(self, experimental_name, modified_method_with_self)
            else:

                @wraps(experimental_method)
                def modified_method_without_self(*args):
                    mod_args = tuple(args[i] for i in index_map)
                    return experimental_method(*args) * modifier_function(*mod_args)

                setattr(self, experimental_name, modified_method_without_self)

        setattr(cls, "apply_modifications", apply_modifications)
        setattr(cls, "create_modified_method", create_modified_method)
        return cls

    return class_decorator
