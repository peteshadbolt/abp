from setuptools import setup, find_packages
from glob import glob
from os import path

STATIC = glob("static/*.*")+glob("static/img/*.*")+glob("static/scripts/*.*")

setup(
    name = "abp",
    version = "0.4.2",
    packages = find_packages(),
    test_suite = "tests",
    author = "Pete Shadbolt",
    author_email = "hello@peteshadbolt.co.uk",
    url = "https://github.com/peteshadbolt/abp",
    description = "Port of C++ due to Simon Anders and Hans J Briegel",
    keywords = "quantum",
    setup_requires = ["numpy"],
    scripts = ["bin/abpserver"],
    install_requires = ["numpy", "networkx", "tqdm", "websocket-client", "websocket-server"],
    package_data = {"abp.static": STATIC}
)
