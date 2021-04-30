from ktypes._abstract_type import KType
from ktypes._token import _Token
from ktypes._error import Error, ErrorHandler

# represents a n-product type from n components given by a dict. retains the order
# of each component, which is used when defining functions out of the n-product type
class kmeta(KType):
    # class attributes
    # [cls.instances] stores the different instances of [kmeta] objects
    #
    # instance attributes
    # [self.name] is the name provided which names the kmeta type
    # [self.dict] is the <dict> which defines the names and types of component
    #       attributes. names are required because the same type can occur in an
    #       n-product type at different indexes/positions
    # [self.keys] is a <list> of all attributes which the kmeta <self> object 
    #       responds to
    # [self.signature] is the ordered <list> of types which uniquely defines the 
    #       type of the kmeta object
    
    instances = {}

    def __init__(self, universe, name, data, predicate=None):
        super().__init__(universe, predicate=predicate)
        self.name = name
        self.dict = data
        self.keys = data.keys()
        self.signature = list(data.values())

    # TODO: formailze this method for kmeta objects
    # returns true if [raw_data] matches the kmeta object <self>.
    def matches(self, raw_data):
        return False

    # construct a token of <self> from [raw_data] which must be a <dict> type. 
    # the token is constructed by matching the named attributes given by the 
    # [raw_data] dict with the named attributes corresponding to the kmeta type
    # <self>. raises an error if these named attributes do not coincide, or if the 
    # component types provided do not satisfy the typechecker
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
