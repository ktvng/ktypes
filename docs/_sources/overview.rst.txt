Overview
========

Type Theory is a formal symbolic system equipped with certain computation rules that 
allow it to express logical and mathematical statements. In simpler terms, 
Type Theory is a language which can clearly and precisely express ideas and rules (think grammar) 
which determine in what ways different to ideas can be combined to form new ideas.

The objects which we manipulate in Type Theory are called **tokens**, and each 
token is given with a unique and fixed type. For programmers familiar with statically typed 
programming languages such as C/C++ or Java, this should make perfect sense; after all, 
this is exactly how we define variables.

The code ``int x;`` in either language defines a token (named ``x``) with a unique and 
fixed type ``int``. It's a fact of life that when programming in C/C++ or Java, you 
can't declare a variable without giving it a type. This is in actually a hold-over from 
the Formal Type Theory which influenced the design of these two programming languages. 
Specifically, variables are actually tokens, and hence must have a unique and 
fixed type. 

In Formal Type Theory, a token ``x`` of a type ``T`` is written as ``x : T``, and 
we follow this convention throughout. Translating the above statment into this 
style, we could alternatively write ``x : int``. Readers with a discerning eye will notice that 
this is exactly how Python function annotations are written.

.. code-block:: python

    def sum(x : int, y : int) -> int:
        return x + y

Again we see Formal Type Theory influencing programming languages! Even Python, 
a dynamically-typed language, isn't immune to this influence.