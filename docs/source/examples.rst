.. _examples:

========
Examples
========

Examples are provided as `Jupyter <https://jupyter.org/>`_ notebooks in a separate
`signac-examples <https://github.com/glotzerlab/signac-examples>`_ repository.
These notebooks may be launched `interactively on Binder <https://mybinder.org/v2/gh/glotzerlab/signac-examples/master?filepath=index.ipynb>`_
or downloaded and run on your own system.
Visualization of data is done via `Matplotlib <https://matplotlib.org/>`_ unless otherwise noted.

This is a collection of example projects which are designed to illustrate how to implement certain applications and solutions with **signac**.
Unlike the tutorial, the examples consist mainly of complete, immediately executable source code with less explanation.

Workflow Examples
=================

.. toctree::
    :maxdepth: 1
    :glob:

    signac-examples/notebooks/signac_1*


.. todo::

    Add Pumpkin example.
    Add MD with Gromacs example.

Analysis Examples
=================

The examples below include examples of using **signac** to analyze data, as well as ways of integrating with other software such as pandas and sacred.


.. toctree::
    :maxdepth: 1
    :glob:

    signac-examples/notebooks/signac_2*
