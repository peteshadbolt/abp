from setuptools import setup
from glob import glob
from os import path

STATIC = glob("abp/static/*.*")+glob("abp/static/img/*.*")+glob("abp/static/scripts/*.*")

setup(
    name = "abp",
    version = "0.4.26",
    packages = ["abp", "abp.static"],
    test_suite = "tests",
    author = "Pete Shadbolt",
    author_email = "hello@peteshadbolt.co.uk",
    url = "https://github.com/peteshadbolt/abp",
    description = "Port of C++ due to Simon Anders and Hans J Briegel",
    keywords = "quantum",
    setup_requires = ["numpy"],
    scripts = ["bin/abpserver"],
    install_requires = ["numpy", "networkx", "tqdm", "websocket-client", "websocket-server"],
    package_data = {"abp.static": STATIC},
    include_package_data=True
)
