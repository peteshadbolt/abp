.. abp documentation master file, created by
   sphinx-quickstart on Sun Jul 24 18:12:02 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2


Welcome to ``abp``
===============================

This is the documentation for ``abp``. It's a work in progress.

``abp`` is a Python port of Anders and Briegel' s `method <https://arxiv.org/abs/quant-ph/0504117>`_ for fast simulation of Clifford circuits. 
That means that you can make quantum states of thousands of qubits, perform any sequence of Clifford operations, and measure in any of :math:`\{\sigma_x, \sigma_y, \sigma_z\}`.
It should do thousands of qubits without much trouble.

Installing
----------------------------

You can install from ``pip``:

.. code-block:: bash

   $ pip install --user abp

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

It's pretty easy to build a graph state, act some gates, and do measurements::

    >>> from abp import GraphState
    >>> g = GraphState(range(5))
    >>> for i in range(5):
    ...     g.act_hadamard(i)
    ... 
    >>> for i in range(4):
    ...     g.act_cz(i, i+1)
    ... 
    >>> print g 
    0:  IA	(1,)
    1:  IA	(0,2)
    2:  IA	(1,3)
    3:  IA	(2,4)
    4:  IA	(3,)
    >>> print g.to_state_vector()
    |00000>: 0.18+0.00j
    |00001>: 0.18+0.00j ...
    >>> g.measure(2, "px")
    0
    >>> print g
    0:  IA	(3,)
    1:  ZC	(3,)
    2:  IA	-
    3:  ZA	(0,1,4)
    4:  IA	(3,)

GraphState
-------------------------

The ``abp.GraphState`` class is your main interface to ``abp``.  
Here follows complete documentation

.. autoclass:: abp.GraphState

    .. automethod:: abp.GraphState.__init__

    .. automethod:: abp.GraphState.add_node

    .. automethod:: abp.GraphState.add_nodes

    .. automethod:: abp.GraphState.act_local_rotation

    .. automethod:: abp.GraphState.act_hadamard

    .. automethod:: abp.GraphState.act_cz

    .. automethod:: abp.GraphState.add_edge

    .. automethod:: abp.GraphState.add_edges

    .. automethod:: abp.GraphState.del_edge

Reference
----------------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

