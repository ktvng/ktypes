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
support ingesting a string format as the data instance"

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
will always throw an error. Unlike C/C++ or Java, KTypes does not support type coercion.

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
function are in fact curried functions. Formal functions can be evaluated with either the 
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
this procedure to be a binary operation on two component types, due to the prevalence  
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
to the ``schema`` which was used to construct the n-product type, but replacing the 
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
logic of left/right injections which, in a formal Type-Theoretic setting, construct 
tokens of the coproduct type, the coproduct constructor is a binary operation on 
two known types. Currently the coproduct constructor is non-commutative, and thus 
the coproduct types ``A | B`` and ``B | A`` are distinct. 

Coproduct types can also be understood as "or" types, hence the bar "or-operator" 
used in the syntax of the coproduct constructor. As a result, constructing a coproduct 
type is quite intuitive:

.. code-block:: python

    types.person_or_errormsg = types.person | types.str

    print(types.person_or_errormsg)
    # person | str

A token of a coproduct type can be constructed by passing in one of the allowable types 
of the coproduct into the constructor. Building on the previous examples:

.. code-block:: python

    coprod_token1 = types.person_or_errormsg(types.str("error"))
    coprod_token2 = types.person_or_errormsg(person_token))

    print(coprod_token1)
    # inr(error : str) : person | str

    print(coprod_token2)
    # inl([Charles : str, 21 : int] : person) : person | str


Product Functions
-----------------

Beyond grouping relevant data together, product types are also useful as they permit 
formally typed functions to be defined over them. Functions defined over product 
types can be single-domain typed to avoid any unnecessary complications with currying 
and multiple arguments. 

The KTypes library includes a built-in product function constructor which takes in a 
curried formal function and outputs a single-domain typed formal function defined 
over the product type inferred from the input function's signature.

As an example, give some function ``f : int -> int -> int``, supplying ``f`` as the 
input to the KTypes product function constructor would yield a single-domain typed 
formal function defined on the product type ``int % int``. In other words, we would 
obtain ``f' : int & int -> int`` which only takes one argument, a token of the product 
type ``int & int``.

The product function construct can be called from the ``types`` module as demonstrated 
below:

.. code-block:: python

    # define the product type
    types.int_pair = {
        "a": types.int,
        "b": types.int,
    }

    @types.function
    def sum(x : types.int, y : types.int) -> types.int:
        return x + y 
    
    prod_sum = types.ind_prod(sum)

    print(sum)
    # sum : int -> int -> int

    print(prod_sum)
    # klambda : int_pair -> int


Coproduct Functions
-------------------

Similarly, the KTypes library gives the power to define functions out of coproduct 
types. The syntax is aliased to the pipe (``|``) operator, and provides a modular 
approach that allows reduces ``if/else`` clutter when defining such functions.

Given a coproduct type ``A | B`` and two functions ``f : A -> C`` and ``g : B -> C`` 
the KTypes library interprets the well-defined expression ``f | g`` as defining 
a new function out of the coproduct type ``A | B`` whose operation is uniquely defined 
by evaluating either ``f`` or ``g``. In other words, ``f | g`` is a formally typed 
function and we express it as ``f | g : A | B -> C``. 

.. note:: 

   While Formal Type Theory does not distinguish between simple types, their closure 
   under products/coproducts, and formal function types, the KTypes library does not currently 
   permit the inclusion of formal functions in products/coproducts. Effectively, the 
   library enforces a strict differentiation between data and data manipulations. 

   Thus, there should be no ambiguity when the pipe operator is used. When ``A`` is a 
   simple type and ``f`` is a formal function, the operation ``A | f`` is not well 
   defined an will throw an exception.


In defining formal functions out of coproduct types in this way, there are three 
requirements to ensure the well-formed-ness of the expression ``f | g``. 

#. Both functions ``f`` and ``g`` must land in the same type.
#. Both functions ``f`` and ``g`` must not be defined over the same domain.
#. Both functions ``f`` and ``g`` must be single-domain typed functions. They may 
   not curry arguments.

Of course it is assumed that both ``f`` and ``g`` are formal functions notated by the 
``types.function`` decorator. The follow example shows this construction in practice:

.. code-block:: python

    types.int_or_str = types.int | types.str

    @types.function
    def f(x : types.int) -> types.str:
        return types.str("It is an integer")

    @types.function
    def g(x : types.str) -> types.str:
        return types.str("String is '") + x + types.str("'")

    to_str = f | g

    print(to_str)
    # klambda : int | str -> str

    token = types.int_or_str("hello")
    print(to_str(token))
    # It was a string 'hello' : str

Predicates
==========

The KTypes library also provides functionality to define **subtypes** out of pre-existing 
types within the type universe. Subtypes are built from existing types but enforce a 
custom defined boolean predicate which is checked at runtime to ensure type-correctness.

Predicates can be user defined functions or lambda expressions, which take in as their 
sole argument the piece or raw data which should be evaluated, and returns true or false 
depending on if the raw data matches. Predicated types are created as follows using the 
``.where(...)`` attribute method.

.. code-block:: python

    def is_na(raw_data):
        return raw_data == "N/A"

    types.nan = types.str.where(predicate=is_na)

    print(types.nan.matches("hello"))
    # False
    
    print(types.nan.matches("N/A"))
    # True

In the example above, we see that ``types.nan`` is a user-defined subtype of the 
primitive type ``str`` where the only token of the type is ``"N/A"``. Because 
predicates are simple Python methods, the provide additional power and usability 
to the KTypes framework. More complex predicates can enforce regex matching, gate 
ranges and specific values, or even be used to model enums.

Parsing
=======

The primary goal of the KTypes library is to facilitate the ingesting and processing 
of ad-hoc data formats. These are sources of data which result from possibly real-world 
sources which may be incomplete, corrupt, or unstandardized. Our goals is to bring these 
ad-hoc data formats into a well typed environment where reasoning and manipulations can 
be made precise. 

As a result, the KTypes framework takes inspiration and follows much of the design 
as the `PADS project <https://dl.acm.org/doi/10.1145/1938551.1938556>`_. Specifically, 
we introduce a built-in parser to assist in the automated ingestion of ad-hoc data 
formats. Data can be directly parsed into a type using an instance of the the 
`types.parser` class, which takes in a known type and a parse format specification 
string.

A parse format specification string is a Python `str` which describes how a known 
type should be translated into a string raw data representation. Currently, the parser 
is only compatible with product types built from primitive/or types, but this is an active 
domain for development. 

Each attribute of the product type should be enclosed in ``$`` (dollar signs), and 
any non-enclosed characters are treated as delimiters which complete the data 
representation. The following example demonstrates a typical ``.csv`` format for the 
``user`` product type.

.. code-block:: python

    types.user = {
        "name": types.str,
        "age": types.int,
        "email": types.str, 
    }

    parse_format = "$name$, $age$, $email$\n"

Given the ``user`` type and the ``parse_format`` as above, constructing a KTypes 
parser is simple:

.. code-block:: python

    parser = types.parser(types.user, parse_format)

The type specification and parse format specification are abstracted into separate 
entities to allow various data formats all to be parsed into the same underlying type, 
which reduces the need to modify downstream code. Thus, changes to the data source 
can in general be handled by updating the parse format, reducing the risk of propagating 
changes to downstream code and logic.

The ``parser`` can then be used to parse raw string data into well-formed known types. 
Specifically, ``parser`` will create tokens of the ``user`` type. 

A parser has two methods of parsing raw string data: **instance** and **stream**

Instance
--------

The ``.parse_instance(...)`` method takes in a Python ``str`` object and greedily 
parses out a single token. The following example illustrates how it works. Given the 
``parser`` as defined above:

.. code-block:: python

    raw_data = "John Howerson, 42, howerson@email.org\n ignored content"
    result = parser.parse_instance(raw_data)

    print(result)
    # [John Howerson : str, 42 : int, howerson@email.org : str] : user

The output of ``.parse_instance(...)``, if the parsing succeeds, is a well-formed 
token of the type supplied when the ``parser`` was defined. This can then be used 
as an input to any formal function and all KTypes manipulations are supported.

Notice that ``raw_data`` must not totally match the type, and greedy parsing ensures 
that the longest-first matching substring of ``raw_data`` is used. Longest-first is 
the longest substring after the first match, where all in-between substrings are 
also matches. 

In other words, the parse will keep consuming characters until a match is encountered. 
If the next (lookahead) character causes a match failure, then this substring will 
be used as the raw data instance; otherwise, the parser will continue consuming 
characters and building up the raw data instance until the lookahead token induces 
a match failure.

Stream 
------

The KTypes parser is also available as a stream parser. Using the ``.parse_stream(...)`` 
method, the parser will ingest the supplied raw string data instance and store all parsed 
tokens as a list. This is a persistent list, so long as the ``reset`` argument is not 
set to ``True``. 

The ``.parse_stream(...)`` method returns a window to this persistent list after each 
call, thus all tokens can be obtained by saving the final return value of the method. 

The following example demonstrates these two features.

.. code-block:: python

    raw_data1 = "John Howerson, 42, howerson@email.org\nBob Billins, 23, bill@mail.com\n"
    result = parser.parse_stream(raw_data)
    print(result)

    for r in result:
        print(r)
    # [John Howerson : str, 42 : int, howerson@email.org : str] : user
    # [Bob Billins : str, 23 : int, bill@mail.com : str] : user

    result = parser.parse_stream("James Ray")
    result = parser.parse_stream(", 31", ")
    result = parser.parse_stream("ray.j@mailmain.edu\n")

    for r in result:
        print(r):
    # [John Howerson : str, 42 : int, howerson@email.org : str] : user
    # [Bob Billins : str, 23 : int, bill@mail.com : str] : user
    # [James Raw : str, 31 : int, ray.j@mailmain.edu : str] : user
