from ktypes._abstract_type import KType
from ktypes._token import _Token
from ktypes._error import Error, ErrorHandler

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

        if isinstance(raw_data, dict):
            for key in self.keys:
                data = raw_data.get(key, None)
                if data is not None and data.is_a(self.dict[key]):
                    token_dict[key] = raw_data[key]
                else:
                    return ErrorHandler.take(Error.OfTypeMismatch(expected=self.dict[key], got=data))
        else:
            return ErrorHandler.take(Error.OfArgument(expected_type=type({}), got=raw_data))

        return _Token(token_dict, self)

