# abp 0.4.22
Python port of Anders and Briegel' s [method](https://arxiv.org/abs/quant-ph/0504117) for fast simulation of Clifford circuits. 

## Documentation
You can read the full documentation [here](https://peteshadbolt.co.uk/abp/). You can also build it locally using Sphinx with `make doc`.

## Installation
It's easiest to install with `pip`:

```shell
$ pip install --user abp==0.4.22
```

Or clone and install in `develop` mode:

```shell
$ git clone https://github.com/peteshadbolt/abp.git
$ cd abp
$ python setup.py develop --user
$ python setup.py develop --user --prefix=  # Might be required on OSX
```

