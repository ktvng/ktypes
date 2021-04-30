from ktypes._abstract_type import KType
from ktypes._token import _Token

# basic ktype for integer values
class kint(KType):
    # class attributes:
    # [instances] stores different instances of the <kint> type whcih may 
    #       arise from predicate application. key is a unique hash code obtained
    #       from the supplied predicate used to determine if two predicates
    #       or predicate types are equal.
    #
    # instance attributes:
    # [name] of the ktype

    # see top level documentation
    instances = {}

    # create the type <kint>. only called initially to generate the global
    # KTypes.int type, and when a [predicate] is applied
    def __init__(self, universe, predicate=None):
        super().__init__(universe, predicate=predicate)
        self.name = "int"

    # TODO: allow raw_data to be other formats than string
    # construct an instance of <kint> from [raw_data]
    def construct(self, raw_data):
        return _Token(int(raw_data), self)

    # returns True if [raw_data] type matches <self>
    def matches(self, raw_data):
        if " " in raw_data:
            return False

        try:
            int(raw_data)
            return self.predicate(raw_data)
        except Exception:
            return False

    # assumes both [token1] and [token2] are tokens of <self> type
    # returns the addition product both
    def add(self, token1, token2):
        return _Token(token1.value + token2.value, self)

    # assumes both [token1] and [token2] are tokens of <self> type
    # returns the subtraction product both
    def subtract(self, token1, token2):
        return _Token(token1.value - token2.value, self)

    # assumes both [token1] and [token2] are tokens of <self> type
    # returns the multiplication product both
    def multiply(self, token1, token2):
        return _Token(token1.value * token2.value, self)

    # assumes both [token1] and [token2] are tokens of <self> type
    # returns the division product both
    def divide(self, token1, token2):
        return _Token(token1.value / token2.value, self)
        