# KnownTypes (KTypes)
A high-level, type-theoretic data annotation language built into Python 3

## Overview
KTypes or KnownTypes is a an open-source library which provides a framework to 
formally define complex data types and functions between data types inside a 
formal type theoretic framework.

The type-specified universe coexists with the standard Python type system, 
allowing for seamless switching between formally typed functions and traditional 
pythonic methods. Runtime type-checking and library recursors serve as tools 
that ensure type correctness. A library parser is provided to facilitate the 
pipeline of ad-hoc data into the formal typed setting of KTypes.

## Install
KTypes is still in the pre-alpha phase.
It can be installed through `pip`. With `python3` installed, simply run the 
following command.
```
python3 -m pip install ktypes
```

## Tests
Tests are written in a lightweight, custom (read: informal) unit-test framework, and can be run via the following command in the root directory
```
python3 runtests.py
```

## Usage
To use KTypes in your file, simply import the `types` submodule from the `ktypes` 
module as below. All types inhereted through the `types` submodule
```python
from ktypes import types
```

KTypes currently supports two built in primitive data types, `int` and `str`.
Creating a token (an instance of a type) is simple:
```python
x = types.int(42)
print(x)
# 42 : int
```

Formal function types can be created by decorating annotated python3 methods 
with the `types.function` decorator
```python
@types.function
def sum(x : types.int, y : types.int) -> types.int:
    return x + y

print(sum)
# sum : int -> int -> int
```

Formal functions are by default curried functions, but also support multiple 
arguments as a shorthand for currying
```python
y = types.int(8)

print(sum(x)(y))
# 50 : int

add8 = sum(y)
print(add8)
# lambda<sum> : int -> int
```