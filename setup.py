from setuptools import setup, find_packages

setup(
    name = "abp",
    version = "0.1",
    packages = find_packages(),
    test_suite = 'tests',
    author = "Pete Shadbolt",
    author_email = "hello@peteshadbolt.co.uk",
    description = "Implements Anders and Briegel in Python",
    license = "MIT",
    keywords = "quantum",
    url = "https://github.com/peteshadbolt/abp/"
)
