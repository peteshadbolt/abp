# abp 0.5.0
Python port of Anders and Briegel' s [method](https://arxiv.org/abs/quant-ph/0504117) for fast simulation of Clifford circuits.

## Documentation
You can read the full documentation [here](https://peteshadbolt.co.uk/abp/). You can also build it locally using Sphinx with `make doc`.

To install Sphinx on OSX, use `pip install sphinx`. If after doing so `make doc` still does not work, some OSX users may also need to install `sphinxcontrib-napoleon` by running `pip install sphinxcontrib-napoleon`.

## Installation
It's easiest to install with `pip`:

```shell
$ pip install --user abp==0.5.0
```

Or install from source: clone and install in `develop` mode:

```shell
$ git clone https://github.com/peteshadbolt/abp.git
$ cd abp
$ python setup.py develop --user
$ python setup.py develop --user --prefix=  # Might be required on OSX
```
If installed from source, check that abp is running your local Python install by ensuring that the first line of `abp/bin/abpserver` matches your local python install (which can be found using `which python`). If not, you will need to change it to your local python path.

Some OSX users may find they need additional modifications to their path to execute `abpserver` from the command line. To add `abpserver` to your path, you must first find where it is installed, e.g. by typing:

```shell
$ find / -iname "abpserver"
```
A path to a Python library, such as `/Users/username/Library/Python/2.7/bin/abpserver`, should appear (if installed from source, this is not `path/to/repo/abp/bin/abpserver`). To add this to your path permanently, open `~/.bash_profile`, add the path, e.g. `export PATH="$HOME/Library/Python/2.7/bin:$PATH"` and restart your shell. If this has worked, typing `which abpserver` will display the desired path.


