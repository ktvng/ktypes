========
Concepts
========

A zero-to-sixty guide on getting up to speed with the KTypes Library.

Getting Started
===============

Install the KTypes library with ``pip``

.. code-block:: bash

    $ python3 -m pip install ktypes

To use the KTypes library, import the ``types`` submodule:

.. code-block:: python

    from ktypes import types

All known types, primitive and user-defined, are available as attributes of the 
``types`` module. This provides a simple interface by which the formal types can be 
accessed while avoiding name collisions between Python objects and KTypes types. 

Primitive Types
---------------

Currently KTypes supports three primitive types; ``str``, ``int``, and ``float`` which 
can be accessed by attributing the ``types`` module. Using the same syntax to construct 
instances of standard Python objects, we can construct a new token of a known type. 
All we need to supply is a data instance matching the type we want to construct (e.g. 
for an int, we would supply a Python int), but when in doubt, KTypes constructors all 
support injesting a string format as the data instance"

.. code-block:: python

    x = types.int(42)
    y = types.int("53")

    print(x)
    # 42 : int

    print(y)
    # 53 : int

Primitive types support basic operations (``+|-|*|/``) in the obvious way. If an 
operation is not generally well defined (e.g. subtracting strings), a library error 
will be thrown. Similarly, applying a basic operation on two tokens of different types 
will always throw an error. Unlike C/C++ or Java, KTypes does not support type coersion.

.. code-block:: python

    x = types.int(12)
    y = types.int(4)

    a = types.str("hello")
    b = types.str("world")

    print(x * y)
    # 48 : int 

    print(a + b)
    # helloworld : str

Primitive types can be converted back to standard Python objects to perform unsafe 
operations as well by using the ``.value`` attribute of the token. In general, 
this is not encouraged. All type conversions should be done using the KTypes type-casting 
system (underdevelopment)

.. code-block:: python

    x = types.int(9)
    y = types.int(3 + x.value)

    print(x.value)
    # 3

    print(y)
    # 12 : int


Functions
---------

In addition to type annotations for data, KTypes also supports type annotations for 
functions defined between formally typed data. Using the ``types.function`` decorator, 
we can mark standard Python methods as formally typed functions and use these functions 
in formally typed settings. 

In order for the function decorator to behave properly, decorated functions must 
be fully type specified using the annotation syntax introduced in Python 3

.. code-block:: python

    @types.function
    def twice(x : types.int) -> types.int:
        return x + x

    print(twice)
    twice : int -> int

In the example above, we decorate the fully-annotated method ``twice`` to convert 
it into a formally typed function. The syntax for notating formal function types 
is borrowed from Haskell, as evidenced by the ``__str__`` method defined for the decorated 
``twice`` formal function object. As this notation implies, multiple argument formal 
function are in fact curried functions. Formal functions can be evaluted with either the 
traditional syntax, or with the more 'correct' curried notation

.. code-block:: python

    @types.function
    def sum(x : types.int, y : types.int) -> types.int:
        return x + y

    x = types.int(10)
    y = types.int(20)

    print(sum)
    # sum : int -> int -> int

    print(sum(x, y))
    # 30 : int

    print(sum(x)(y))
    # 30 : int

As expected, partial currying of an argument returns a partially evaluated function 
which can is still a formal function, and which can be used later. Borrowing the ``sum``
function from above:

.. code-block:: python

    add5 = sum(types.int(5))

    print(add5)
    # klambda<sum> : int -> int

    y = add5(types.int(15))
    
    print(y)
    # 20 : int

While there is no requirement that only formal function are used during data 
manipulations, best practice would have it that one *ought always* use formal functions 
to manipulate data. The strength of a formal type system is in the transparency 
and confidence it provides when manipulating data. These benefits would be lost if 
standard Python methods were used instead.

Constructions
=============

Beyond the primitive types and formal function types, the KTypes library also 
supports the type-theoretic construction of product and coproduct types, or, equivalently,
"and" and "or" types, respectively. These methods of constructing new types gives the 
KTypes ecosystem the additional level or expressivity and richness required to represent 
most data schemas.

Product Types
-------------
The first construction is the (Cartesian) Product. Whereas Formal Type Theory defines 
this procedure to be a binary operation on two component types, due to the prevelance 
of product types in real world applications, the KTypes library treats all product types 
as n-products, thus avoiding the unnecessary syntax required to iteratively apply a 
binary product type constructor. 

Constructing a product type is remarkably simple. A ``dict`` is used to encode all 
information required to express the n-product, and passing the dict into the ``types`` 
module is sufficient for the library to complete the type inference and construct the 
appropriate type.

Because two components of an n-product can be the same type, a unique identifier would be 
required to distinguish between them. Solving for this problem, all n-products are defined 
with named components. A ``dict`` handles this association perfectly.

.. code-block:: python

    schema = {
        "name": types.str,
        "age": types.int,
    }

The above ``schema`` defines the information necessary to infer a 2-product type 
containing both ``str`` and ``int`` types. To the object oriented programmer, this 
type of construction should bear a striking resemblance to defining a ``class``. The 
keys in the ``dict`` correspond to the attribute names and the values correspond to the 
formal type of each attribute. 

Given such a ``dict`` such as ``schema`` from above, constructing a product type is easy:

.. code-block:: python

    types.person = schema

    print(types.person)
    # person

This syntax has two key requirements which are not immediately obvious.

#. The attribute name of ``types`` which we are assigning to name the new product type,
   in this case, ``person``, must not already be associated with a type. In other words, redefining 
   named types is not a supported action, but defining a new type is.
#. A ``dict`` must be supplied on the right hand side, and it must be well-formed. 
   That is, it must have attribute names as keys and known types as values. Note that 
   the known type values need not be primitive types. 
   
Note also that the order provided in the ``dict`` is relevant to the definition of 
the n-product type, a different order will product a different n-product type. 

A token of an n-product type can be constructed by supplying a ``dict`` very similar 
to the ``schema`` which was used to consruct the n-product type, but replacing the 
values of the dict with actual tokens of the required type. Once a new type is defined,
it can be accessed by attributing the `types` module. N-product types are constructed 
by the same syntax which constructs instances of standard Python objects. Note that 
the instance data supplied must be the appropriate ``dict`` or a type mismatch error 
will be thrown.

.. code-block:: python

    data = {
        "name": types.str("Charles"), 
        "age": types.int("21")
    }
    
    person_token = types.person(data)

    print(person_token)
    # [Charles : str, 21 : int] : person 

Coproduct Types
---------------

Coproduct types serve the same role as unions in C/C++ and Haskell. Following the 
logic of left/right injections which, in a formal Type Theortic setting, construct 
tokens of the coproduct type, the coproduct constructor is a binary operation on 
two known types. Currently the coproduct constructor is non-commutative, and thus 
the coproduct types ``A | B`` and ``B | A`` are distinct. 

Coproduct types can also be understood as "or" types, hence the bar "or-operator" 
used in the syntax of the coproduct constructor. As a result, constructing a coproduct 
type is quite intuitive:

.. code-block:: python

    types.either_person_or_errormsg = types.person | types.str

    print(types.either_person_or_errormsg)
    # person | str

A token of a coproduct type can be constructed by passing in one of the allowable types 
of the coproduct into the constructor. Building on the previous examples:

.. code-block:: python

    coprod_token1 = types.either_person_or_errormsg(types.str("error"))
    coprod_token2 = types.either_person_or_errormsg(person_token))

    print(coprod_token1)
    # inr(error : str) : person | str

    print(coprod_token2)
    # inl([Charles : str, 21 : int] : person) : person | str
