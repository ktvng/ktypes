from ktypes._abstract_type import KType
from ktypes._token import _Token
from ktypes._error import Error, ErrorHandler


# basic ktype for string values
class kstr(KType):
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

    # create the type <kstr>. only called initially to generate the global
    # KTypes.str type, and when a [predicate] is applied
    def __init__(self, universe, predicate=None):
        super().__init__(universe, predicate=predicate)
        self.name = "str"

    def matches(self, raw_data):
        return self.predicate(raw_data)

    def construct(self, raw_data):
        return _Token(str(raw_data), self)

    def add(self, token1, token2):
        return _Token(token1.value + token2.value, self)

    def subtract(self, token1, token2):
        return ErrorHandler.take(Error.OfBinaryOperation("-", token1.type, token2.type))

    def multiply(self, token1, token2):
        return ErrorHandler.take(Error.OfBinaryOperation("-", token1.type, token2.type))

    def divide(self, token1, token2):
        return ErrorHandler.take(Error.OfBinaryOperation("-", token1.type, token2.type))