.. abp documentation master file, created by
   sphinx-quickstart on Sun Jul 24 18:12:02 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


``abp``
===============================

This is the documentation for ``abp``. It's a work in progress.

.. toctree::
   :hidden:
   :maxdepth: 2

   modules


``abp`` is a Python port of Anders and Briegel' s `method <https://arxiv.org/abs/quant-ph/0504117>`_ for fast simulation of Clifford circuits. 
That means that you can make quantum states of thousands of qubits, perform any sequence of Clifford operations, and measure in any of :math:`\{\sigma_x, \sigma_y, \sigma_z\}`.

Installing
----------------------------

You can install from ``pip``:

.. code-block:: bash

   $ pip install --user abp==0.4.21

Alternatively, clone from the `github repo <https://github.com/peteshadbolt/abp>`_ and run ``setup.py``:

.. code-block:: bash

   $ git clone https://github.com/peteshadbolt/abp
   $ cd abp
   $ python setup.py install --user

If you want to modify and test ``abp`` without having to re-install, switch into ``develop`` mode:

.. code-block:: bash

   $ python setup.py develop --user  

Quickstart
----------------------------

Let's make a new ``GraphState`` object with a register of three qubits:

    >>> from abp import GraphState
    >>> g = GraphState(3)

All the qubits are initialized by default in the :math:`|+\rangle` state:

    >>> print g.to_state_vector()
    |000❭: 	 √1/8	+ i √0
    |100❭: 	 √1/8	+ i √0
    |010❭: 	 √1/8	+ i √0
    |110❭: 	 √1/8	+ i √0
    |001❭: 	 √1/8	+ i √0
    |101❭: 	 √1/8	+ i √0
    |011❭: 	 √1/8	+ i √0
    |111❭: 	 √1/8	+ i √0

We can also check the stabilizer tableau:

    >>> print g.to_stabilizer()
     0  1  2
    ---------
     X      
        X   
           X

Or look directly at the vertex operators and neighbour lists:

    >>> print g
    0:  IA	-
    1:  IA	-
    2:  IA	-

This representation might be unfamiliar. Each row shows the index of the qubit, then the **vertex operator**, then a list of neighbouring qubits. To understand vertex operators, read the original paper by Anders and Briegel.

Let's act a Hadamard gate on the zeroth qubit -- this will evolve qubit ``0`` to the :math:`H|+\rangle = |1\rangle` state:

    >>> g.act_hadamard(0)
    >>> print g.to_state_vector()
    |000❭: 	 √1/4	+ i √0
    |010❭: 	 √1/4	+ i √0
    |001❭: 	 √1/4	+ i √0
    |011❭: 	 √1/4	+ i √0
    >>> print g
    0:  YC	-
    1:  IA	-
    2:  IA	-

And now run some CZ gates:

    >>> g.act_cz(0,1)
    >>> g.act_cz(1,2)
    >>> print g
    0:  YC	-
    1:  IA	(2,)
    2:  IA	(1,)
    >>> print g.to_state_vector()
    |000❭: 	 √1/4	+ i √0
    |010❭: 	 √1/4	+ i √0
    |001❭: 	 √1/4	+ i √0
    |011❭: 	-√1/4	+ i √0

Tidy up a bit:

    >>> g.del_node(0)
    >>> g.act_hadamard(0)
    >>> print g.to_state_vector()
    |00❭: 	 √1/2	+ i √0
    |11❭: 	 √1/2	+ i √0

Cool, we made a Bell state. Incidentally, those those state vectors and stabilizers are genuine Python objects, not just stringy representations of the state:

    >>> g = abp.GraphState(2)
    >>> g.act_cz(0, 1)
    >>> g.act_hadamard(0)
    >>> psi = g.to_state_vector()
    >>> print psi
    |00❭: 	 √1/2	+ i √0
    |11❭: 	 √1/2	+ i √0

``psi`` is a state vector -- i.e. it is an exponentially large vector of complex numbers. We can still run gates on it:

    >>> psi.act_cnot(0, 1)  
    >>> psi.act_hadamard(0)
    >>> print psi
    |00❭: 	 √1	+ i √0

But these operations will be very slow. Let's have a look at the stabilizer tableau:

    >>> tab = g.to_stabilizer()
    >>> print tab
     0  1
     ------
     Z  Z
     X  X
    >>> print tab.tableau
    {0: {0: 3, 1: 3}, 1: {0: 1, 1: 1}}
    >>> print tab[0, 0]
    3


GraphState API
-------------------------

The ``abp.GraphState`` class is the main interface to ``abp``.  

.. autoclass:: abp.GraphState
    :special-members: __init__
    :members:

.. _clifford:

The Clifford group
----------------------

.. automodule:: abp.clifford

|

The ``clifford`` module provides a few useful functions:

.. autofunction:: abp.clifford.use_old_cz
    :noindex:

Visualization
----------------------

``abp`` comes with a tool to visualize graph states in a WebGL compatible web browser (Chrome, Firefox, Safari etc). It uses a client-server architecture.

First, run ``abpserver`` in a terminal:

.. code-block:: bash

    $ abpserver
    Listening on port 5000 for clients..

Then browse to ``http://localhost:5001/`` (in some circumstances ``abp`` will automatically pop a browser window).

Now, in another terminal, use ``abp.fancy.GraphState`` to run a Clifford circuit::

    >>> from abp.fancy import GraphState
    >>> g = GraphState(10)
    >>> g.act_circuit([(i, "hadamard") for i in range(10)])
    >>> g.act_circuit([((i, i+1), "cz") for i in range(9)])
    >>> g.update()

And you should see a 3D visualization of the state. You can call ``update()`` in a loop to see an animation.

Reference
----------------------------

More detailed docs are available here:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

