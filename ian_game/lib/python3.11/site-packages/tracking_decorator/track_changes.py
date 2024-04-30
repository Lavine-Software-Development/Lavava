from tracking_decorator.trash_collections import trash_collection

def track_changes(*attributes):
    def class_decorator(cls):
        original_init = cls.__init__

        def make_getter(attribute_name):
            storage_name = '_' + attribute_name
            def getter(self):
                return getattr(self, storage_name)
            return getter

        def make_setter(attribute_name, attribute_to_track):
            storage_name = '_' + attribute_name
            def setter(self, value):

                if getattr(self, storage_name) != value:
                    self.tracked_attributes.add(attribute_to_track)

                    if isinstance(value, (list, set, dict)):
                        TrashCollection = trash_collection(value)
                        setattr(self, storage_name, TrashCollection)
                    else:
                        setattr(self, storage_name, value)
            return setter

        for attribute in attributes:
            if isinstance(attribute, tuple):
                attribute, attribute_to_track = attribute
                getter_func = make_getter(attribute)
                setter_func = make_setter(attribute, attribute_to_track)
            else:
                getter_func = make_getter(attribute)
                setter_func = make_setter(attribute, attribute)
            setattr(cls, attribute, property(getter_func, setter_func))

        # Modify the __init__ to initialize properties
        def new_init(self, *args, **kwargs):
            self.tracked_attributes = set()

            for attribute_name in attributes:
                if isinstance(attribute_name, tuple):
                    attribute_name = attribute_name[0]
                storage_name = '_' + attribute_name
                setattr(self, storage_name, None)

            original_init(self, *args, **kwargs)
            self.clear()

        def clear(self):
            self.tracked_attributes.clear()
        
        cls.__init__ = new_init
        cls.clear = clear
        return cls
    
    return class_decorator