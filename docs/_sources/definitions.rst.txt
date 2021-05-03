===========
Definitions
===========

Type/Known Type
===============
Defining a type is more or less a philosophical (read: ontological) problem. In a 
sense, a type embodies some abstract, universalizing category or classification. A type :math:`T`
can be thought of as a property which chan be shared by one or many particulars, each 
of which would be said to have type :math:`T`.

The above definition is appealing in its simplicity, but it obscures the fact that a type 
should be understood as more intrinsic an a mere property. Rather, the type of an object 
conveys some essential characteristic; each object can only have one type. 

This relationship can be colloquially expressed with the "is a(n)" relation. If an object 
:math:`s` has type :math:`T`, (denoted by the judgement :math:`s : T`), then we can say 
:math:`s` is a(n) :math:`T`. Concretely, given the judgement :math:`x : \text{int}`, we 
can that :math:`x` is a(n) :math:`\text{int}`. 

Again, while this relation is simple and expressive, one must be careful in that 
while everyday objects can have multiple "is a(n)" relations, a type is fixed and 
unique. So while we can speak of a person, say Susan, both with "Susan is a person", and 
"Susan is a student", this is disallowed in Formal Type Theory. Each object/particular 
may only have one type. 

While this may seem restrictive in some senses, it is actually a very powerful notion. 
If we know that :math:`x` is a(n) :math:`\text{int}`, that is, if we have the judgement 
:math:`x : \text{int}`, then even without knowing what the variable :math:`x` is specifically, 
we already know that we use addition, multiplication, etc, or that we can compare :math:`x` 
to another integer :math:`y`. All of this knowledge stems from the fact that :math:`x : \text{int}` 
is a powerful judgement: the :math:`\text{int}` type conveys a lot of information. 

In the KTypes library, a **known type** is the terminology used when talking about a 
formally expressed type which is defined in a way such that the KTypes library can interpret 
it and its properties. The KTypes library has three primitive known types built-in, 
``types.int``, ``types.str``, and ``types.float``, defined in this way to avoid collisions 
with the standard Python implementations of ``int``, ``str``, and ``float``, which 
are not usable in the KTypes framework and hence "unknown types".

Token
=====

A token is an instance or a particular object of a type. In the judgment :math:`s : T`, 
we know that :math:`T` is a type, and correspondingly, we also get that :math:`s` is 
a token of this type. 

Of course, a given type may have many different tokens. As an example, we can write 
the two judgments :math:`42 : \text{int}` and :math:`12 : \text{int}`, which tells us 
that both :math:`42` and :math:`12` are tokens of the :math:`\text{int}` type. 

Formal Function
===============

A formal function is Python method which has been appropriately defined and decorated 
in order for the KTypes framework to interpret it as a well-typed token of a function 
type. While formal functions are simply Python methods at core, and obey standard 
Pythonic syntax, they are useful because they ensure that data manipulations on known 
types are well behaved; formal functions are subject to runtime type-checking, and by 
using formal functions, one can be confident that one's data manipulations preserve 
certain defined type relationships.

Formal functions are tokens of function types. Type theoretically, functions are notated 
by the judgement :math:`f : A \to B`. This judgement tells us that a function :math:`f` 
has domain :math:`A` and range :math:`B`. Printing formal functions of the KTypes library 
follows this notation, one would see ``f : A -> B``. Note that :math:`A` and :math:`B` 
must be known types.

Formal functions also curry by default.

Currying
--------

Currying is the technique by which methods defined with multiple arguments can be 
represented by formal functions. In the definition of a formal function above, there is 
no simple way to express a function defined from two types. That is, the judgement 
:math:`f : A, A' \to B` is not well defined. Instead, currying is employed. 

Recall that formal functions are tokens of a function type. Given :math:`f : A \to B`, 
we can say that :math:`f` is a token of type :math:`A \to B` where :math:`A` and :math:`B` 
are both known types.

We can make a similar statement given the judgement :math:`g : A' \to C`. The key insight, 
then, is that the known types :math:`A, A', B, C` have no restrictions built in. Thus 
because :math:`A \to B` is itself a type, we can treat it as such. In fact, we can 
even let the type :math:`C` be this type, :math:`A \to B`.

What we would obtain is the function :math:`g : A' \to (A \to B)`. This statements 
states that :math:`g` is a function which takes in a token of type :math:`A'` and 
returns a *function* from :math:`A \to B`. This function moreover, has access 
to the value which was supplied into :math:`g`, and one can see that we have effectively 
defined a function over two types. 

As is standard practice, we omit the parenthesis when providing the judgement for 
:math:`g` and instead write `g : A' \to A \to B`


Signature
---------

A signature is a representation of either a product type or a function type. A 
signature, plus the knowledge of whether a type is product or function, supplies 
the necessary information to infer the exact designation of the type. In product 
types, schema is often used synonymously with signature, highlighting the similarity 
of product types to database schemas.

Product Type
============

The Cartesian product of two sets :math:`A, B` is the set of ordered pairs :math:`(a, b)` 
where :math:`a` is taken from :math:`A` and :math:`b` taken from :math:`B`. The product 
type on types parallels this construction.

Coproduct Type
==============

The coproduct on types :math:`A, B` is effectively the "or" or "union" of two types. 
That is, a token of the coproduct type denoted :math:`A | B` is the either a token of 
:math:`A`, or :math:`B` which has been injected into the coproduct type using the 
:math:`inl` or :math:`inr` functions, standing for left/right injection, respectively.