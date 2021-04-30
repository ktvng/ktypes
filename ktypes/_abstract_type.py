import ktypes._kor as _kor
from ktypes._error import Error, ErrorHandler

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
    def __init__(self, universe, predicate=None):
        self.universe = universe
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
            return self
        
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
            pred_ktype = klass(self.universe, predicate=predicate)
            klass.instances[predicate_hash] = pred_ktype
            self.universe.add_type(str(self), pred_ktype, hash=predicate_hash)
            
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
        universe = a.universe
        existing_kor = universe.get_or(a, b)

        if existing_kor is None:
            existing_kor = _kor.kor(universe, a, b)

        universe.add_type("or", existing_kor, hash=hash(existing_kor))
        return existing_kor

    # returns a string representation of the type <self> 
    def __str__(self):
        return self.name + self._predicate_designation()
        