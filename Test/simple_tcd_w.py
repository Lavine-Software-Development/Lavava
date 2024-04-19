def watch_attributes(*attrs):
    def decorator(cls):
        class WrappedClass:

            tracked_attrs = list(attrs) + getattr(cls, 'tracked_attrs', [])

            def __init__(self, *args, **kwargs):
                self._original = cls(*args, **kwargs)
                self.updated = set()
                
                for attr in self.tracked_attrs:
                    # Ensure attribute exists before creating a property
                    if hasattr(self._original, attr):
                        setattr(self.__class__, attr, self.create_property(attr))
                    else:
                        raise AttributeError(f"Attribute {attr} not found in {cls.__name__}")
                
            def create_property(self, attr):

                def getter(self):
                    return getattr(self._original, attr)
                
                def setter(self, value):
                    old_value = getattr(self._original, attr)
                    if old_value != value:
                        self.updated.add(attr)
                    setattr(self._original, attr, value)
                
                return property(getter, setter)
            
            def clear(self):
                self.updated.clear()

        return WrappedClass
    return decorator
