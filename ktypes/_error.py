# wrapper to handle errors thrown inside the KTypes library. allows user to define 
# the action taken when an error is thrown. currently supports either
#   [raise]: raises the error
#   [pass]: pass the error to the calling function as the return value
class ErrorHandler():
    # class attributes
    # [cls.handler_response_instruct] is a <str> which takes the value
    #       "raise"
    #       "pass"
    #       and determines the action the ErrorHandler takes when an error thrown
    #       by the KTypes library is caught
    # [recognized_instructs] are the recognized strings for the
    #       'handler_response_instruct'

    handler_reponse_instruct = "raise"
    recognized_instructs = [
        "raise",
        "pass",
    ]

    # change the 'handler_response_instruct' globally for the KTypes library
    @classmethod
    def set_response_instruct(cls, instruct="raise"):
        if instruct in cls.recognized_instructs:
            cls.handler_reponse_instruct = instruct
            return
        raise Exception("unsupported error handler instruct")

    # takes in a library error and responds depending on the defined 
    # 'handler-resonse-instruct' instruction
    @classmethod
    def take(cls, err):
        if cls.handler_reponse_instruct == "raise":
            raise err
        elif cls.handler_reponse_instruct == "pass":
            return err

    # always raises the error passed to the <ErrorHandler>
    @classmethod
    def raises(cls, err):
        raise err

# functions as the namespace for all KTypes library errors
class Error():
    # error OfTypeMismatch is thrown when a type is [expected] but a different type
    # was [got] 
    class OfTypeMismatch(Exception):
        def __init__(self, expected="", got=""):
            self.expected = expected
            self.got = got

        def __str__(self):
            return f"type mismatch: expected <{str(self.expected)}> but got <{str(self.got)}>"

    # error OfBinaryOperation is thrown when a binary operation is not well defined
    # between [type1] and [type2]
    class OfBinaryOperation(Exception):
        def __init__(self, op, type1, type2):
            self.op = op
            self.type1 = type1
            self.type2 = type2

        def __str__(self):
            return f"unsupported operand types: cannot '{str(self.op)}' <{str(self.type1)}> with <{str(self.type2)}>"

    # error OfExpectedToken is thrown when a token is expected but some non-token
    # [obj] is given instead
    class OfExpectedToken(Exception):
        def __init__(self, obj):
            self.obj = obj

        def __str__(self):
            return f"expected token of a type, but got {type(self.obj)}"

    # error OfArgument is thrown when some argument is [expected]<str> but a different
    # argument of python type [got]<obj>. 
    class OfArgument(Exception):
        def __init__(self, expected_type=None, got=None):
            self.expected = expected_type
            self.got = got

        def __str__(self):
            return f"expected argument of {str(self.expected)} but got {type(self.got)}"

    # error OfOrConstructorFailure is thrown when the '|' (or-operator) is used
    # incorrectly
    class OfOrConstructorFailure(Exception):
        def __init__(self, msg):
            self.msg = msg

        def __str__(self):
            return f"invalid 'or' usage: {self.msg}"

    # error OfUndefinedAttribute is thrown when a product type token of [ktype] is 
    # indexed with [attr] but does not have [attr] as an attribute, as defined
    class OfUndefinedAttribute(Exception):
        def __init__(self, attr, ktype):
            self.attr = attr
            self.type = ktype

        def __str__(self):
            return f"invalid attribute: product type <{str(self.type)}> has no attribute '{self.attr}'"

    # error OfUncallable is thrown when an attempt is made to call an
    # uncallable type
    class OfUncallable(Exception):
        def __init__(self, msg):
            self.msg = msg

        def __str__(self):
            return f"<{str(self.msg)}> is not callable"