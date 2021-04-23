from ktypes._abstract_type import KType
from ktypes._kint import kint
from ktypes._kstr import kstr
from ktypes._kfunc import kfunc
from ktypes._kor import kor
from ktypes._kmeta import kmeta

class kuniverse(KType):
    def __init__(self, index):
        super().__init__(None)
        self.index = index
        self.name = f"Univ_{index}"
        self.types = {"int": kint(self), "str": kstr(self)}

    def where(self, predicate):
        return self

    def matches(self, raw_data):
        return False

    def construct(self, raw_data):
        return self

    def add_type(self, name, ktype, hash=""):
        self.types[name + str(hash)] = ktype

    def get_function(self, signature):
        for name, ktype in self.types.items():
            if isinstance(ktype, kfunc) and ktype.signature == signature:
                return ktype
        func = kfunc(self, signature)
        self.add_type(func.name, func)

        return func

    def get_meta(self, signature):
        for name, ktype in self.types.items():
            if isinstance(ktype, kmeta) and ktype.signature == signature[:-1]:
                return ktype
        
        # TODO: handle case where kmeta does not exist
        return None            

    def _add_type_to_dict(self, ktype, d):
        if isinstance(ktype, kor):
            self._add_type_to_dict(ktype.left, d)
            self._add_type_to_dict(ktype.right, d)
        else:
            d[ktype] = 1

    def get_or(self, a, b):
        or_dict = {}
        self._add_type_to_dict(a, or_dict)
        self._add_type_to_dict(b, or_dict)

        for name, ktype in self.types.items():
            if isinstance(ktype, kor):
                candidate_or_dict = {}
                self._add_type_to_dict(ktype, candidate_or_dict)
                if candidate_or_dict == or_dict:
                    return ktype

        # TODO: handle case where kor does not exist
        return None
