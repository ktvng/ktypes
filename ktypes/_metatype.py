from ktypes._kmeta import kmeta

# metaclass to allow the <KTypes> class to handle unknown attributes, set new 
# types by simple assignment, and record/name user defined types
#
# named types are immutable; after binding a type to a <KTypes> attribute, that
# type can no longer be modified
class MetaType(type):
    # set a <KType> attribute to refer to a type; disallow mutability for 
    # previously bound attribute
    def __setattr__(self, name, value):
        if not name in self.universe.types:
            if isinstance(value, dict):
                value = kmeta(self.universe, name, value)
            self.universe.add_type(name, value)
            return

        raise Exception("named type is already defined")

    # return type by name
    def __getattr__(self, name):
        for kname, ktype in self.universe.types.items():
            if kname == name:
                return ktype
        return None


