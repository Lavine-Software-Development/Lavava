def track_changes(tracked_set_name, *tracked_attrs):
    def class_decorator(cls):
        def make_attr_property(attr):
            private_attr_name = f"__{attr}"

            def getter(self):
                return getattr(self, private_attr_name, None)

            def setter(self, value):
                setattr(self, private_attr_name, value)
                tracked_set = getattr(self, tracked_set_name, set())
                tracked_set.add(attr)
            
            return property(getter, setter)

        for attr in tracked_attrs:
            setattr(cls, attr, make_attr_property(attr))
        
        return cls
    
    return class_decorator