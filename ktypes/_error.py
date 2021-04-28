class ErrorHandler():
    # either:
    #   "raise"
    #   "pass"
    handler_reponse_instruct = "raise"
    recognized_instructs = [
        "raise",
        "pass",
    ]

    @classmethod
    def set_response_instruct(cls, instruct="raise"):
        if instruct in cls.recognized_instructs:
            cls.handler_reponse_instruct = instruct
            return
        raise Exception("unsupported error handler instruct")


    @classmethod
    def take(cls, err):
        if cls.handler_reponse_instruct == "raise":
            raise err
        elif cls.handler_reponse_instruct == "pass":
            return err

    @classmethod
    def raises(cls, err):
        raise err


class Error():
    class OfTypeMismatch(Exception):
        def __init__(self, expected="", got=""):
            self.expected = expected
            self.got = got

        def __str__(self):
            return f"type mismatch: expected <{str(self.expected)}> but got <{str(self.got)}>"

    class OfBinaryOperation(Exception):
        def __init__(self, op, type1, type2):
            self.op = op
            self.type1 = type1
            self.type2 = type2

        def __str__(self):
            return f"unsupported operand types: cannot '{str(self.op)}' <{str(self.type1)}> with <{str(self.type2)}>"

    class OfExpectedToken(Exception):
        def __init__(self, obj):
            self.obj = obj

        def __str__(self):
            return f"expected token of a type, but got {type(self.obj)}"

    class OfOrConstructorFailure(Exception):
        def __init__(self, msg):
            self.msg = msg

        def __str__(self):
            return f"invalid 'or' usage: {msg}"