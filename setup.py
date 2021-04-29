from setuptools import find_packages, setup

setup(
    name='ktypes',
    package_dir= {'ktypes/ktypes': 'ktypes'},
    packages=find_packages(include=['ktypes']),
    version='0.0.3',
    description='Type Theoretic Data Annotations',
    author='Kevin Tang',
    license='MIT',
    install_requires=[],
)