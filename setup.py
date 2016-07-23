from setuptools import setup, find_packages
from glob import glob
from os import path

APPNAME = "abp"
STATIC = glob("static/*.*")+glob("static/img/*.*")+glob("static/scripts/*.*")
appdata = path.expanduser(path.join("~", "." + APPNAME))
print appdata

setup(
    name = "abp",
    version = "0.3",
    packages = find_packages(),
    test_suite = "tests",
    author = "Pete Shadbolt",
    description = "Port of C++ due to Simon Anders and Hans J Briegel",
    keywords = "quantum",
    setup_requires = ["numpy"],
    scripts = ["bin/abpserver"],
    install_requires = ["numpy", "networkx", "tqdm", "websocket-client", "websocket-server"],
    data_files = [("static", STATIC)]
)
