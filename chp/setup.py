import os
from setuptools import setup, Extension, find_packages

path = "chp.c"
chp = Extension("chp", [path])

extensions = [chp]

setup(
    name="chp",
    version="0.1",
    packages=find_packages(),
    ext_modules=extensions,
    author="Scott Aaronson & Daniel Gottesman",
    description="Ported by Pete Shadbolt",
    license="Copyright Scott Aaronson"
)

