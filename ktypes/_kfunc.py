from ktypes._abstract_type import KType
from ktypes._token import _Token
from ktypes._error import Error, ErrorHandler

# represents a function/curried-function for multiple arguments
class kfunc(KType):
    # ktypes is a list of ktypes with the final ktype being the returned value
    def __init__(self, universe, signature):
        super().__init__(universe)
        self.signature = signature
        self.name = self._name()

    def _name(self):
        ktype_names = list(map(lambda x: str(x), self.signature))
        return " -> ".join(ktype_names)

    def where(self, predicate):
        pass

    def construct(self, raw_data):
        return _function_wrapper(func)

    def matches(self, raw_data):
        return False



class _function_wrapper():
    def __init__(self, func, ktype, args=[], kwargs={}):
        super().__init__()
        self.ktype = ktype
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def _typecheck(self, arg, ktype):
        if ktype is None:
            raise Exception("internal: missing type")

        if isinstance(arg, _Token):
            if not arg.is_a(ktype):
                ErrorHandler.raises(Error.OfTypeMismatch(expected=ktype, got=arg))
        
        return True

    def _get_type_after_currying(self, old_ktype):
        signature = old_ktype.signature[1:]
        if len(signature) == 1:
            return signature[0] 
        else:
            return self.ktype.universe.get_function(signature)

    def _curry(self, arg):
        _, required_type = list(self.func.__annotations__.items())[len(self.args)]
        self._typecheck(arg, required_type)
        curried_type = self._get_type_after_currying(self.ktype)
        if isinstance(curried_type, kfunc):
            curried_func = _function_wrapper(self.func, curried_type, args=self.args+[arg], kwargs=self.kwargs)
            return _Token(curried_func, curried_type, is_func=True)
        else:
            result = self.func(*(self.args + [arg]), **self.kwargs)
            self._typecheck(result, self.func.__annotations__.get("return", None))
            return result


    def wrap(universe):
        def inner_wrap(func):
            signature = list(func.__annotations__.values())
            function_type = universe.get_function(signature)
            return _Token(_function_wrapper(func, function_type), function_type, is_func=True)

        return inner_wrap

    def __call__(self, *args, **kwargs):
        curried_func = self
        if args or kwargs:
            for arg in args:
                curried_func = curried_func._curry(arg)

        return curried_func

    def __or__(a, b):
        if len(a.ktype.signature) != 2 or len(b.ktype.signature) != 2:
            return ErrorHandler.take(Error.OfOrConstructorFailure("cannot 'or' curried-functions"))

        a_returns = a.ktype.signature[-1]
        b_returns = b.ktype.signature[-1]

        if a_returns != b_returns:
            return ErrorHandler.take(Error.OfOrConstructorFailure("cannot 'or' functions with differing return types"))

        a_domain_type = a.ktype.signature[0]
        b_domain_type = b.ktype.signature[0]

        if a_domain_type == b_domain_type:
            return ErrorHandler.take(Error.OfOrConstructorFailure("cannot 'or' functions defined over the same domain"))

        @_function_wrapper.wrap(a.ktype.universe)
        def klambda(x : a_domain_type | b_domain_type) -> a_returns:
            inj, token = x.value
            if(token.is_a(a_domain_type)):
                return a(token)
            else:
                return b(token)

        return klambda

