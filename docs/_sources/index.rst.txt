.. KTypes documentation master file.

KnownTypes Documentation
========================

KnownTypes or KTypes is a an Python open-source library which provides a framework to 
define data and functions types inside a formal type theoretic framework. Typed-specified
objects and contexts coexist with standard dynamically-typed Python statements, 
allowing for seemelss transitions between formally-typed and dynamically-typed 
code. Robust runtime type-checking ensures type-correctness during data manipulations.

All KTypes annotations are built into the standard Python syntax, and the entire 
KTypes type-universe is implemented natively, making KTypes quick and easy for both 
experienced and novice Python developers to pick and master.

This webpage provides in-depth documentation and a zero-to-sixty tutorial behind 
the basics of Formal Type Theory and how KTypes leverages these concepts. Working through 
these tutorial pages provides the user everything they need to understand the 
fundemental logic of the KTypes system in order both appreciate Formal Type Theory and 
get started using the KTypes library in their own Python projects.

* Start with the **Overview** to gain a better understanding of Formal Type Theory, 
  and why everyone should use formal type specifications in critical path code
* Check on the **Definitions** for a reference on terminology
* **Concepts** introduces more detailed Type Theory in the context of the KTypes library 
  and its own implementation. Jump to here if you have a working understanding of Type 
  Theory and just want to see how the KTypes library works in action.

********
Contents
********

.. toctree::
   :maxdepth: 3

   overview
   definitions
   concepts

*************
Version Notes
*************
The KTypes library is currently in the pre-alpha phase (V0.0.xx). All framework API are subject 
to change without notice. Please do not integrate KTypes into your projects just yet! 

******
Author
******
The KTypes library is written and maintained by Kevin Tang (ktvng). If you would like to 
contribute, please check us out on `Github <https://github.com/ktvng/ktypes>`_.