# metaclass to allow the <KTypes> class to handle unknown attributes, set new 
# types by simple assignment, and record/name user defined types
#
# named types are immutable; after binding a type to a <KTypes> attribute, that
# type can no longer be modified
class MetaType(type):
    # set a <KType> attribute to refer to a type; disallow mutability for 
    # previously bound attribute
    def __setattr__(self, name, value):
        if not name in self.universe:
            if isinstance(value, dict):
                value = KTypes.kmeta(name, value)
            self._add_type_to_universe(name, value)
            return

        raise Exception("named type is already defined")

    # return type by name
    def __getattr__(self, name):
        for kname, ktype in self.universe.items():
            if kname == name:
                return ktype
        return None

# TODO: make token instances unique
# wrapper class for the KTypes module; used to allow for custom attribute
# handling when defining new named types
class KTypes(metaclass=MetaType):
    ############################################################################
    ############################################################################
    ############################################################################
    # meta-structural methods

    # abstract class which is inherited by all types of the known type system. 
    # types are represented as instances of classes inheriting from <KType>
    class KType():
        # instance attributes:
        # [self.predicate] boolean function which must be satisfied by all
        #       tokens of the type
        # [self.predicate_hash] hash value of the predicate function used to
        #       test for type equality between predicate types
        # [self.has_predicate] <True> if a predicate function is supplied

        # initialize a type, possibly with a boolean [predicate] function which
        # must be satisfied by tokens of the type
        def __init__(self, predicate=None):
            self.predicate = predicate
            self.predicate_hash = hash(predicate)
            self.has_predicate = True
            if predicate is None:
                self.predicate = self._default_predicate
                self.has_predicate = False

        # constructs a token of this type. 
        def __call__(self, *args, **kwargs):
            return self.construct(*args, **kwargs)

        # inbuilt predicate enforcing the raw string representation of the type 
        # has a length equal to [size]
        def _where_size_eq(self, size):
            def f(raw_data):
                return len(raw_data) == size

            return f

        # inbuild predicate enforcing the raw string representation of the type
        # ends whenever the [end] character is reached
        def _where_ends_on(self, end):
            def f(raw_data):
                return end not in raw_data
            
            return f

        # generates a function to handle matching multiple predicates, where 
        # a token is only valid if all predicates are satisfied. will operate
        # via short-circuit computation
        def _multiple_predicate(self, preds):
            def f(raw_data):
                for pred in preds:
                    if not pred(raw_data):
                        return False
                return True

            return f

        # generate a new type resulting from applying a [predicate], a fixed size
        # equal to [size_eq], and/or termination on [ends_on] to an existing
        # type. will return existing predicate type if found.
        def where(self, predicate=None, size_eq=None, ends_on=None):
            if predicate is None and size_eq is None and ends_on is None:
                raise Exception("predicate required")
            
            predicates = []
            hashable_rep = []
            if predicate is not None:
                predicates.append(predicate)
                hashable_rep.append(predicate)
            if size_eq is not None:
                predicates.append(self._where_size_eq(size_eq))
                hashable_rep.append(f"size_eq={size_eq}")
            if ends_on is not None:
                predicates.append(self._where_ends_on(ends_on))
                hashable_rep.append(f"ends_on={ends_on}")

            if len(predicates) > 1:
                predicate_hash = hash(tuple(hashable_rep))
                predicate = self._multiple_predicate(predicates)
            elif len(predicates) == 1:
                predicate_hash = hash(hashable_rep[0])
                predicate = predicates[0]

            klass = type(self)
            pred_ktype = klass.instances.get(predicate_hash, None)
            if pred_ktype is None:
                pred_ktype = klass(predicate)
                klass.instances[predicate_hash] = pred_ktype
                KTypes._add_type_to_universe(str(self), pred_ktype, hash=predicate_hash)
             
            return pred_ktype

        # contruct a token of type <self>
        def construct(self, raw_data):
            pass
        
        # default predicate accepts all tokens
        def _default_predicate(self, arg):
            return True

        # string used to designate the presence of a predicate in the __str__ 
        # method, for printing purposes only.
        def _predicate_designation(self):
            return "*" if self.has_predicate else ""

        # override to alias the '|' operator to construct an or-type between 
        # types [a] and [b]
        def __or__(a, b):
            existing_kor = KTypes._get_kor_in_universe(a, b)
            if existing_kor is None:
                existing_kor = KTypes.kor(a, b)

            KTypes._add_type_to_universe("or", existing_kor, hash=hash(existing_kor))
            return existing_kor

        # returns a string representation of the type <self> 
        def __str__(self):
            return self.name + self._predicate_designation()

    # class used to represent tokens of a given type. contains a value of some 
    # data and a reference to the type of that value.
    #
    # value can either be:
    #   <dict> to indicate <kmeta> types
    #   <_function_wrapper> to indicate <kfunc> types
    #   <tuple> to indicate <kor> types 
    class Token():
        # instance attributes:
        # [self.value] the value of the data referenced by this token
        # [self.type] the known type of the data
        # [self._is_meta] true if this token encodes a <kmeta> type
        # [self._is_func] true if this token encodes a <kfunc> type
        # [self._is_or] true if this token encodes a <kor> type

        # construct a token with [value] for a given [ktype] 
        def __init__(self, value, ktype):
            self.value = value
            self.type = ktype
            self._is_meta = True if isinstance(value, dict) else False
            self._is_func = True if isinstance(value, KTypes._function_wrapper) else False
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
            if not isinstance(o, KTypes.Token):
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

        # TODO: implement
        def __or__(a, b):
            if a._is_func and b._is_func:
                return a.value | b.value

            raise Exception("cannot or tokens of non-function types")

    class _function_wrapper():
        def __init__(self, func, ktype, args=[], kwargs={}):
            super().__init__()
            self.ktype = ktype
            self.func = func
            self.args = args
            self.kwargs = kwargs

        def _curry(self, arg):
            _, required_type = list(self.func.__annotations__.items())[len(self.args)]
            KTypes._typecheck(arg, required_type)
            curried_type = KTypes._get_type_after_currying(self.ktype)
            if isinstance(curried_type, KTypes.kfunc):
                curried_func = KTypes._function_wrapper(self.func, curried_type, args=self.args+[arg], kwargs=self.kwargs)
                return KTypes.Token(curried_func, curried_type)
            else:
                result = self.func(*(self.args + [arg]), **self.kwargs)
                KTypes._typecheck(result, self.func.__annotations__.get("return", None)) 
                return result

        # TODO: this is not updating self.ktype to the new ktype.
        # TODO: this should also ensure that each curried arg is right
        def __call__(self, *args, **kwargs):
            curried_func = self
            if args or kwargs:
                for arg in args:
                    curried_func = curried_func._curry(arg)

            return curried_func

        def __or__(a, b):
            if len(a.ktype.signature) != 2 or len(b.ktype.signature) != 2:
                raise Exception("cannot 'or' curried-functions")

            a_returns = a.ktype.signature[-1]
            b_returns = b.ktype.signature[-1]

            if a_returns != b_returns:
                raise Exception("cannot 'or' functions with different return values")

            a_domain_type = a.ktype.signature[0]
            b_domain_type = b.ktype.signature[0]

            if a_domain_type == b_domain_type:
                raise Exception("cannot 'or' functions defined over the same domain")

            @KTypes.function
            def klambda(x : a_domain_type | b_domain_type) -> a_returns:
                inj, token = x.value
                if(token.is_a(a_domain_type)):
                    return a(token)
                else:
                    return b(token)


            return klambda

            
            




    ############################################################################
    ############################################################################
    ############################################################################
    # ktypes

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
        def __init__(self, predicate=None):
            super().__init__(predicate)
            self.name = "int"

        # TODO: allow raw_data to be other formats than string
        # construct an instance of <kint> from [raw_data]
        def construct(self, raw_data):
            return KTypes.Token(int(raw_data), self)

        # returns True if [raw_data] type matches <self>
        def matches(self, raw_data):
            if " " in raw_data:
                return False

            try:
                int(raw_data)
                return self.predicate(raw_data)
            except Exception:
                return False

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
        def __init__(self, predicate=None):
            super().__init__(predicate)
            self.name = "str"

        def matches(self, raw_data):
            return self.predicate(raw_data)

        def construct(self, raw_data):
            return KTypes.Token(str(raw_data), self)





    # represents a function/curried-function for multiple arguments
    class kfunc(KType):
        # ktypes is a list of ktypes with the final ktype being the returned value
        def __init__(self, signature):
            super().__init__()
            self.signature = signature
            self.name = self._name()

        def _name(self):
            ktype_names = list(map(lambda x: str(x), self.signature))
            return " -> ".join(ktype_names)

        def where(self, predicate):
            pass

        def construct(self, raw_data):
            return KTypes._function_wrapper(func)

        def matches(self, raw_data):
            return False

    # represents a coproduct (or) type from two component types 
    class kor(KType):
        instances = {}

        def __init__(self, left, right, predicate=None):
            super().__init__(predicate)
            self.name = str(left) + " | " + str(right) 
            self.left = left
            self.right = right

        def where(self, predicate):
            self.predicate = predicate
            return self

        def matches(self, raw_data):
            return self.left.matches(raw_data) or self.right.matches(raw_data)

        def construct(self, raw_data):
            if self.left.matches(raw_data):
                return self._inl(self.left.construct(raw_data))
            elif self.right.matches(raw_data):
                return self._inr(self.right.construct(raw_data))

        def _inl(self, token):
            return KTypes.Token(("inl", token), self)

        def _inr(self, token):
            return KTypes.Token(("inr", token), self)

    # represents a n-product type from n components given in a dict
    class kmeta(KType):
        instances = {}

        def __init__(self, name, data, predicate=None):
            super().__init__(predicate)
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

            return KTypes.Token(token_dict, self)

    class knone(KType):
        instances = {}

        def __init__(self):
            super().__init__()
            self.name = "None"

        def construct(self, raw_data):
            raise Exception("cannot construct token of KType.None")
        
        def matches(self, raw_data):
            raise Excpetion("cannot match token of KType.None")


    class kuniverse(KType):
        def __init__(self, index):
            super().__init__(None)
            self.index = index
            self.name = f"universe {index}"
            self.ktypes = []

        def where(self, predicate):
            return

        def matches(self, raw_data):
            return False

        def construct(self, raw_data):
            return







    ############################################################################
    ############################################################################
    ############################################################################
    # module global helper methods

    universe = {"int": kint(), "str": kstr(), "none": knone()}

    # add [ktype] to the universe with [name] and [hash] defining the dict key
    def _add_type_to_universe(name, ktype, hash=""):
        KTypes.universe[name+str(hash)] = ktype
        

    def _get_function_in_universe(signature):
        for name, ktype in KTypes.universe.items():
            if isinstance(ktype, KTypes.kfunc) and ktype.signature == signature:
                return ktype
        func = KTypes.kfunc(signature)
        KTypes._add_type_to_universe(func.name, func)

        return func

    def _get_kmeta_in_universe(signature):
        for name, ktype in KTypes.universe.items():
            if isinstance(ktype, KTypes.kmeta) and ktype.signature == signature[:-1]:
                return ktype
        
        # TODO: handle case where kmeta does not exist
        return None

    def _add_type_to_dict(ktype, d):
        if isinstance(ktype, KTypes.kor):
            KTypes._add_type_to_dict(ktype.left, d)
            KTypes._add_type_to_dict(ktype.right, d)
        else:
            d[ktype] = 1

    def _get_kor_in_universe(a, b):
        or_dict = {}
        KTypes._add_type_to_dict(a, or_dict)
        KTypes._add_type_to_dict(b, or_dict)

        for name, ktype in KTypes.universe.items():
            if isinstance(ktype, KTypes.kor):
                candidate_or_dict = {}
                KTypes._add_type_to_dict(ktype, candidate_or_dict)
                if candidate_or_dict == or_dict:
                    return ktype

        # TODO: handle case where kor does not exist
        return None

    def _typecheck(arg, ktype):
        if ktype is None:
            raise Exception("missing type")

        if isinstance(arg, KTypes.Token):
            if not arg.is_a(ktype):
                raise Exception("type mismatch")
        
        else:
            if isinstance(ktype, KTypes.KType):
                raise Exception("type mismatch")
            else:
                if not isinstance(arg, ktype):
                    raise Exception("type mismatch")
        
        return True

    def _get_type_after_currying(old_ktype):
        signature = old_ktype.signature[1:]
        if len(signature) == 1:
            return signature[0] 
        else:
            return KTypes._get_function_in_universe(signature)

    ############################################################################
    ############################################################################
    ############################################################################
    # module public interface

    def function(func):
        signature = list(func.__annotations__.values())
        function_type = KTypes._get_function_in_universe(signature)
        return KTypes.Token(KTypes._function_wrapper(func, function_type), function_type)

    def ind_prod(func):
        ktype = KTypes._get_kmeta_in_universe(func.ktype.signature)

        @KTypes.function
        def klambda(x : ktype) -> func.ktype.signature[-1]:
            return func(*list(x.value.values()))
        
        return klambda

    def product(dict_spec):
        name = " & ".join(map(str, dict_spec.values()))
        ktype = KTypes.kmeta(name, dict_spec)
        KTypes._add_type_to_universe(name, ktype, hash=hash(tuple(dict_spec.values())))
        return ktype






















    ############################################################################
    ############################################################################
    ############################################################################
    # parsing

    class parser():
        def __init__(self, ktype, parse_format):
            # TODO: check proper types here

            self.ktype = ktype
            self.parse_format = parse_format
            self._unpack_parse_format()

            self.stream_context = None
            self.stream_tokens = []

        class _unpack_state():
            BASE = 0
            KEYWORD = 1
            
        def _unpack_parse_format(self):
            state = self._unpack_state.BASE
            fragments = []
            fragment = ""

            for c in self.parse_format:
                if c == "$" and state == self._unpack_state.BASE:
                    state = self._unpack_state.KEYWORD
                    
                    # don't add any empty fragments 
                    if not fragment:
                        continue

                    fragments.append(fragment)
                    fragment = ""
                    continue

                elif c == "$" and state == self._unpack_state.KEYWORD:
                    ktype = self.ktype.dict.get(fragment, None)
                    if ktype is None:
                        raise Exception("unknown type keyword")
                    fragments.append((fragment, ktype))
                    fragment = ""
                    state = self._unpack_state.BASE
                    continue
                    
                fragment = fragment + c

            if fragment:
                fragments.append(fragment)


            self.parse_fragments = fragments

        class _parse_context():
            def __init__(self, fragments):
                self.fragments = fragments
                self.clear()

            def clear(self):
                self.position_in_fragment = 0
                self.fragments_index = 0
                self.current_fragment = self.fragments[0]
                self.fragment_is_str = 1 if isinstance(self.current_fragment, str) else 0
                self.token = ""
                self.elements = {}

            def next_fragment(self):
                self.token = ""
                self.position_in_fragment = 0
                self.fragments_index = self.fragments_index + 1
                if self.fragments_index == len(self.fragments):
                    return False

                self.current_fragment = self.fragments[self.fragments_index]

                if isinstance(self.current_fragment, str):
                    self.fragment_is_str = True
                else:
                    self.fragment_is_str = False

                return True

            def match(self, c, lookahead):
                has_next_fragmnet = True
                if self.fragment_is_str:
                    if c != self.current_fragment[self.position_in_fragment]:
                        return {"result": False, "code": "failed to match text delimiter"}

                    self.position_in_fragment = self.position_in_fragment + 1

                    if self.position_in_fragment == len(self.current_fragment):
                        has_next_fragmnet = self.next_fragment()
                else:
                    # proceed by greedy, first-failure-stop, matching
                    name, ktype = self.current_fragment
                    self.token = self.token + c
                    if ktype.matches(self.token) and lookahead is None:
                        self.elements[name] = ktype.construct(self.token)
                        has_next_fragmnet = self.next_fragment()
                    elif ktype.matches(self.token) and not ktype.matches(self.token + lookahead):
                        self.elements[name] = ktype.construct(self.token)
                        has_next_fragmnet = self.next_fragment()

                if not has_next_fragmnet:
                    return {"result": True, "code": "success", "elements": self.elements}

                return None

        def parse_instance(self, instance):
            context = self._parse_context(self.parse_fragments)
            for i in range(len(instance)):
                lookahead = None if i + 1 == len(instance) else instance[i+1]
                result = context.match(instance[i], lookahead)
                if result is not None:
                    return self.ktype.construct(result["elements"])

        def parse_stream(self, stream, reset=False):
            if reset or self.stream_context is None:
                self.stream_context = self._parse_context(self.parse_fragments)
                self.stream_tokens = []

            for i in range(len(stream)):
                lookahead = None if i + 1 == len(stream) else stream[i+1]
                r = self.stream_context.match(stream[i], lookahead)
                if r is not None:
                    if r["result"]:
                        self.stream_tokens.append(self.ktype.construct(r["elements"]))
                        self.stream_context.clear()
                    else:
                        return result

            return self.stream_tokens
