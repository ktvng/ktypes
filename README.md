# KnownTypes (KTypes)
A high-level, type-theoretic data annotation language built into Python 3

## Overview
KnownTypes or KTypes is a an Python open-source library which provides a framework to 
define data and functions types inside a formal type theoretic framework. Typed-specified
objects and contexts coexist with standard dynamically-typed Python statements, 
allowing for seemelss transitions between formally-typed and dynamically-typed 
code. Robust runtime type-checking ensures type-correctness during data manipulations.

All KTypes annotations are built into the standard Python syntax, and the entire 
KTypes type-universe is implemented natively, making KTypes quick and easy for both 
experienced and novice Python developers to pick and master.

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
module as below. All types inherited through the `types` submodule
```python
from ktypes import types
```

See [here](https://ktvng.github.io/ktypes/) for in-depth documentation on how to 
understand and use the KTypes library. 

## Demo
You can run a simple demo file which showcases some of the core functionality of 
the KTypes library with the following command
```
python3 rundemo.py
```
