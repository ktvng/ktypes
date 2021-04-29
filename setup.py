"""KTypes: Type Theoretic Data Annotations

KTypes or KnownTypes is a an open-source library which provides a framework to 
formally define complex data types and functions between data types inside a 
formal type theoretic framework.

The type-specified universe coexists with the standard Python type system, 
allowing for seamless switching between formally typed functions and traditional 
pythonic methods. Runtime type-checking and library recursors serve as tools 
that ensure type correctness. A library parser is provided to facilitate the 
pipeline of ad-hoc data into the formal typed setting of KTypes.

"""

DOCLINES = (__doc__ or '').split("\n")

from setuptools import find_packages, setup

setup(
    name='ktypes',
    package_dir= {'ktypes/ktypes': 'ktypes'},
    packages=find_packages(include=['ktypes']),
    version='0.0.1',
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    project_urls={
        "Source Code": "https://github.com/ktvng/ktype",
        "Bug Tracker": "https://github.com/ktvng/ktype/issues"
    },
    author='ktvng',
    license='MIT',
    install_requires=[],
    python_requires=">=3.6",
)