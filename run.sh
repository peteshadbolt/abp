#!/bin/bash
rm -r abp.egg-info
rm -r build
rm -r dist

python setup.py build sdist

tar -tvf dist/abp-0.4.5.tar.gz
