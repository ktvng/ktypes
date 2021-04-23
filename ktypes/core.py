from ktypes._kor import kor
from ktypes._token import _Token
from ktypes._kint import kint
from ktypes._kstr import kstr
from ktypes._kmeta import kmeta
from ktypes._kfunc import (kfunc, _function_wrapper)
from ktypes._kuniverse import kuniverse

from ktypes._parser import _parser

from ktypes._abstract_type import KType
from ktypes._metatype import MetaType


# TODO: make token instances unique
# wrapper class for the KTypes module; used to allow for custom attribute
# handling when defining new named types
class KTypes(metaclass=MetaType):
    ############################################################################
    ############################################################################
    ############################################################################
    # module public interface
    Token = _Token
    parser = _parser
    universe = kuniverse(index=0)
            

    def function(func):
        return _function_wrapper.wrap(KTypes.universe)(func)

    def ind_prod(func):
        ktype = KTypes.universe.get_meta(func.ktype.signature)

        @KTypes.function
        def klambda(x : ktype) -> func.ktype.signature[-1]:
            return func(*list(x.value.values()))
        
        return klambda

    def product(dict_spec):
        name = " & ".join(map(str, dict_spec.values()))
        ktype = kmeta(KTypes.universe, name, dict_spec)
        KTypes.universe.add_type(name, ktype, hash=hash(tuple(dict_spec.values())))
        return ktype





 



