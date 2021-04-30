from ktypes._abstract_type import KType
from ktypes._token import _Token
from ktypes._error import Error, ErrorHandler

# represents a function/curried-function for multiple arguments. this is the formal
# KTypes representatio nof a function, and is a formal type in the KTypes universe
class kfunc(KType):
    # instance variables
    # [self.signature] is 'signature' of the function. a function signature is 
    #       defined as a list of all (ordered) inputs to a function, terminated by
    #       the return value of the function. it contains all information to 
    #       treat a function as a curried function, where currying one imput 
    #       "returns" another function.
    # [self.name] is the name of the function type, human readable

    # see top-level documentation for the format of [signature]
    def __init__(self, universe, signature):
        super().__init__(universe)
        self.signature = signature
        self.name = self._name()

    # constructs the human readable function name
    def _name(self):
        ktype_names = list(map(lambda x: str(x), self.signature))
        return " -> ".join(ktype_names)

    # functions do not support predicates; currently returns the original function
    # TODO: should return error instead
    def where(self, predicate):
        return self

    # constructs an instance of a function type by wrapping [func] inside a 
    # <_function_wrapper> inside [self.universe]
    def construct(self, func):
        return _function_wrapper.wrap(self.universe)(func)

    # functions do not support matching against raw_data; currently always returns False
    # TODO: should return error instead
    def matches(self, raw_data):
        return False


# TODO: should formalize support for kwarg type arguments
# immediate wrapper for python methods which allows the represention of the method
# as a proper function type that supports currying
class _function_wrapper():
    # instance variables
    # [self.ktype] is the type of the function 
    # [self.func] is the python method which defines the formally typed function
    # [self.args] is a <list> of the arguments already curried into the typed function
    # [self.kwargs] is a <dict> of the named arguments given to the function

    def __init__(self, func, ktype, args=[], kwargs={}):
        super().__init__()
        self.ktype = ktype
        self.func = func
        self.args = args
        self.kwargs = kwargs

    # ensure that the [arg] provided to the function <self> is a token of [ktype]
    def _typecheck(self, arg, ktype):
        if isinstance(arg, _Token):
            if not arg.is_a(ktype):
                ErrorHandler.raises(Error.OfTypeMismatch(expected=ktype, got=arg))
        
        return True

    # get the type of the function returned after currying the next argument 
    # of a function of type [old_ktype]
    def _get_type_after_currying(self, old_ktype):
        signature = old_ktype.signature[1:]
        if len(signature) == 1:
            return signature[0] 
        else:
            return self.ktype.universe.get_function(signature)

    # curry [arg] and returns a new function (token of function type) of the proper
    # type after currying one argument. ensure that [arg] is the proper type
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

    # providing a [universe], returns a function which wraps a python method (func)
    # into a KTypes function token.
    def wrap(universe):
        def inner_wrap(func):
            signature = list(func.__annotations__.values())
            function_type = universe.get_function(signature)
            return _Token(_function_wrapper(func, function_type), function_type, is_func=True)

        return inner_wrap

    # allow a _function_wrapper to be called and curries the arguments given. 
    # returns either a curried function, or the value of evaluating the pyhton 
    # method
    def __call__(self, *args, **kwargs):
        curried_func = self
        if args or kwargs:
            for arg in args:
                curried_func = curried_func._curry(arg)

        return curried_func

    # syntactic sugar which allows two tokens of a function type to be or-ed
    # together to create a function from an or-type. 
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
