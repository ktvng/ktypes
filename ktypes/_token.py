
from ktypes._error import Error, ErrorHandler
# class used to represent tokens of a given type. contains a value of some 
# data and a reference to the type of that value.
#
# value can either be:
#   <dict> to indicate <kmeta> types
#   <_function_wrapper> to indicate <kfunc> types
#   <tuple> to indicate <kor> types 
class _Token():
    # instance attributes:
    # [self.value] the value of the data referenced by this token
    # [self.type] the known type of the data
    # [self._is_meta] true if this token encodes a <kmeta> type
    # [self._is_func] true if this token encodes a <kfunc> type
    # [self._is_or] true if this token encodes a <kor> type

    # construct a token with [value] for a given [ktype] 
    def __init__(self, value, ktype, is_func=False):
        self.value = value
        self.type = ktype
        self._is_meta = True if isinstance(value, dict) else False
        self._is_func = is_func
        self._is_or = True if isinstance(value, tuple) else False

    # allow tokens which encode <kfunc> types to be callable. defers to the
    # stored function.
    def __call__(self, *args, **kwargs):
        if self._is_func:
            return self.value(*args, **kwargs)
        else:
            raise Exception("token is not callable")

    # test for equality of tokens
    def __eq__(self, o):
        if not isinstance(o, _Token):
            return False
        if o.type != self.type:
            return False
        return self.value == o.value

    # return a string representation for a kmeta type with <dict> value
    def _str_for_kmeta(self):
        return '[' + ", ".join(list(map(lambda x: str(x), self.value.values()))) + ']'

    # return a string representation for a kfunc type with <_function_wrapper> type
    def _str_for_kfunc(self):
        function_name = self.value.func.__name__
        if self.value.args:
            function_name = f"klambda<{function_name}>"
        return function_name

    # return a string representation for a kor type with <tuple> value
    def _str_for_kor(self):
        inj, token = self.value
        return inj + "(" + str(token) + ")"

    # return a string representation for a basic type
    def _str_for_basic(self):
        return str(self.value)

    # default action to return None
    def _no_action():
        return None

    # applys either [kmeta_action], [kfunc_action], or [kor_action] depending
    # on the value type of this token
    def _do_function_on_type(self, 
            kmeta_action=_no_action, 
            kfunc_action=_no_action, 
            kor_action=_no_action, 
            base_action=_no_action,
            args=[]):

        if self._is_meta:
            return kmeta_action(*args)
        elif self._is_func:
            return kfunc_action(*args)
        elif self._is_or:
            return kor_action(*args)
        else:
            return base_action(*args)

    # return a string representation of the token
    def __str__(self):
        token_str = self._do_function_on_type(
            kmeta_action=self._str_for_kmeta,
            kfunc_action=self._str_for_kfunc, 
            kor_action=self._str_for_kor,
            base_action=self._str_for_basic)

        return token_str + " : " + str(self.type)

    # true if <self> is a token of [ktype]
    def is_a(self, ktype):
        if self._is_or:
            inj, val = self.value
            return val.is_a(ktype.left) or val.is_a(ktype.right)
        return self.type == ktype

    # allow tokens which encode <kmeta> types to have attributes. defer to
    # the <kmeta> underlying dict for attribute values.
    def __getattr__(self, name):
        if self._is_meta:
            attr = self.value.get(name, None)
            if attr is None:
                raise Exception("no attribute")
            return attr
        return getattr(self.value, name)

    def __or__(a, b):
        if a._is_func and b._is_func:
            return a.value | b.value

        raise Exception("cannot or tokens of non-function types")

    def _validate_binary_op(self, op, other):
        if not isinstance(other, _Token):
            return ErrorHandler.take(Error.OfExpectedToken(other))
        if self.type != other.type:
            return ErrorHandler.take(Error.OfBinaryOperation(op, self.type, other.type))

        return None

    def __add__(self, other):
        result = self._validate_binary_op("+", other)
        if result is not None:
            return result

        return self.type.add(self, other)

    def __sub__(self, other):
        result = self._validate_binary_op("-", other)
        if result is not None:
            return result

        return self.type.subtract(self, other)

    def __mul__(self, other):
        result = self._validate_binary_op("*", other)
        if result is not None:
            return result

        return self.type.multiply(self, other)

    def __truediv__(self, other):
        result = self._validate_binary_op("/", other)
        if result is not None:
            return result

        return self.type.divide(self, other)