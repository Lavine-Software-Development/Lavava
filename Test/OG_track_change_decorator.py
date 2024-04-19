def track_changes(*args):
    def class_decorator(cls):
        def make_attr_property(attr, attr_to_track):
            private_attr_name = f"__{attr}"

            def getter(self):
                return getattr(self, private_attr_name)

            def setter(self, value):
                setattr(self, private_attr_name, value)
                tracked_set = getattr(self, tracked_set_name)
                tracked_set.add(attr_to_track)
                print(f"just updated {attr_to_track}")
                print(f"Tracked set: {tracked_set}")
            
            return property(getter, setter)
        
        parent_tracked_attrs = ()
        if hasattr(cls, '_tracked_attrs'):
            parent_tracked_attrs = cls._tracked_attrs
        
        if hasattr(cls, '_tracked_set_name'):
            tracked_set_name = cls._tracked_set_name
            cls._tracked_attrs = parent_tracked_attrs + args
        else:
            tracked_set_name, *tracked_attrs = args
            cls._tracked_set_name = tracked_set_name
            cls._tracked_attrs = parent_tracked_attrs + tuple(tracked_attrs)

        for attr in cls._tracked_attrs:
            if isinstance(attr, tuple):
                setattr(cls, attr[0], make_attr_property(*attr))
            else:
                setattr(cls, attr, make_attr_property(attr, attr))
        
        return cls
    
    return class_decorator