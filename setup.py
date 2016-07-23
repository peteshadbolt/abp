from setuptools import setup, find_packages

setup(
    name = "abp",
    version = "0.2",
    packages = find_packages(),
    test_suite = "tests",
    author = "Pete Shadbolt",
    description = "Port of C++ due to Simon Anders and Hans J Briegel",
    keywords = "quantum",
    setup_requires = ["numpy"],
    install_requires = ["numpy", "networkx", "tqdm", "websocket-client", "websocket-server"],
)
