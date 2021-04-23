from ktypes._abstract_type import KType
from ktypes._token import _Token

# represents a n-product type from n components given in a dict
class kmeta(KType):
    instances = {}

    def __init__(self, universe, name, data, predicate=None):
        super().__init__(universe, predicate=predicate)
        self.name = name
        self.dict = data
        self.keys = data.keys()
        self.signature = list(data.values())

    def matches(self, raw_data):
        return False

    def construct(self, raw_data):
        token_dict = {}
        for key in self.keys:
            if raw_data.get(key, None).is_a(self.dict[key]):
                token_dict[key] = raw_data[key]
            else:
                raise Exception("type mismatch")

        return _Token(token_dict, self)

