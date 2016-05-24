from setuptools import setup, find_packages

setup(
    name = "chp",
    version = "0.1",
    packages = find_packages(),
    test_suite = 'tests',
    author = "Scott Aaronson & Daniel Gottesman (Ported by Pete Shadbolt)",
    description = "CNOT Hadamard Phase",
    license = "Copyright Scott & others",
    keywords = "quantum",
    url = "http://www.scottaaronson.com/chp/"
)
