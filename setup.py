from setuptools import setup
from glob import glob
from os import path

setup(
    name = "abp",
    version = "0.6.0",
    packages = ["abp"],
    test_suite = "tests",
    author = "Pete Shadbolt",
    author_email = "hello@peteshadbolt.co.uk",
    url = "https://github.com/peteshadbolt/abp",
    description = "Port of C++ due to Simon Anders and Hans J Briegel",
    keywords = "quantum",
    setup_requires = ["numpy"],
    install_requires = ["numpy", "networkx", "requests"],
)
